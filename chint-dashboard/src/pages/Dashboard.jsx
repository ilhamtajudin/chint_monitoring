import { useEffect, useState } from "react";
// Pastikan di file api.js Anda sudah membuat fungsi getDataPeak
import { getDeviceData, getDataPeak } from "../services/api"; 

import Sidebar from "../components/Sidebar";
import DashboardHeader from "../components/DashboardHeader";
import MetricCard from "../components/MetricCard";
import ChartCard from "../components/ChartCard";
import MultiSelect from "../components/MultiSelect";

export default function Dashboard() {
    const [device, setDevice] = useState("chint_1");
    const [data, setData] = useState([]);
    // 1. STATE BARU: Khusus menampung data dari tabel data_peak
    const [dataPeak, setDataPeak] = useState([]); 
    const [isSidebarOpen, setIsSidebarOpen] = useState(true);

    const [voltageSelected, setVoltageSelected] = useState(["ua", "ub", "uc"]);
    const [currentSelected, setCurrentSelected] = useState(["ia", "ib", "ic"]);
    const [powerSelected, setPowerSelected] = useState(["pt"]);
    const [energySelected, setEnergySelected] = useState(["impep"]);
    // 2. STATE BARU: Pilihan parameter untuk grafik Data Peak
    const [dataPeakSelected, setDataPeakSelected] = useState(["qt", "pft"]); 

    const [isVoltageCurrentOpen, setIsVoltageCurrentOpen] = useState(false);
    const [isPowerEnergyOpen, setIsPowerEnergyOpen] = useState(false);
    // 3. STATE BARU: Untuk toggle open/close accordion Data Peak
    const [isDataPeakOpen, setIsDataPeakOpen] = useState(false); 

    // Fetch data untuk Parameter Utama (chint_1 / chint_2)
    const fetchData = async () => {
        try {
            const result = await getDeviceData(device);
            const formatted = result.reverse().map((item) => ({
                ...item,
                created_at: new Date(item.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            }));
            setData(formatted);
        } catch (err) {
            console.log(err);
        }
    };

    // 4. FUNGSI BARU: Fetch data dari tabel data_peak berdasarkan device terpilih
    const fetchDataPeak = async () => {
        try {
            const result = await getDataPeak(device); 
            
            // Mengelompokkan data berdasarkan waktu (created_at)
            const groupedByTime = result.reduce((acc, item) => {
                // Memformat waktu agar sama dengan data chart lainnya
                const time = new Date(item.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                
                if (!acc[time]) {
                    acc[time] = { created_at: time };
                }
                
                // 1. NORMALISASI HURUF: Mengubah nama parameter dari DB (misal 'Uab', 'Qt') menjadi lowercase ('uab', 'qt')
                const paramName = item.parameter.toLowerCase();
                
                // 2. NORMALISASI DESIMAL: Mengatasi angka dengan string koma (misal "2,919" menjadi 2.919)
                let paramValue = 0;
                if (typeof item.value === 'string') {
                    // Jika ada titik dan koma sekaligus atau hanya koma khas format Indonesia
                    paramValue = parseFloat(item.value.replace(/\./g, '').replace(',', '.'));
                } else {
                    paramValue = parseFloat(item.value);
                }
                
                // Simpan ke dalam objek waktu terkait
                acc[time][paramName] = isNaN(paramValue) ? 0 : paramValue;
                return acc;
            }, {});

            // Ubah hasil grouping objek menjadi Array dan urutkan dari waktu terlama ke terbaru
            const formatted = Object.values(groupedByTime).reverse();
            
            console.log("Data Peak Berhasil Diformat:", formatted); // Cek log ini di inspect console browser
            setDataPeak(formatted);
        } catch (err) {
            console.log("Error fetch data peak:", err);
        }
    };

    useEffect(() => {
        fetchData();
        fetchDataPeak(); // Jalankan saat pertama kali atau saat device berubah
        
        const interval = setInterval(() => {
            fetchData();
            fetchDataPeak(); // Polling setiap 5 detik
        }, 5000);
        
        return () => clearInterval(interval);
    }, [device]);

    const latest = data[data.length - 1] || {};

    return (
        <div className="flex min-h-screen bg-[#0b1329] text-slate-100 font-sans overflow-x-hidden">
            
            {/* SIDEBAR */}
            <Sidebar 
                currentDevice={device} 
                isOpen={isSidebarOpen} 
                setIsOpen={setIsSidebarOpen} 
            />

            {/* MAIN CONTENT */}
            <main className="flex-1 p-6 md:p-8 overflow-y-auto transition-all duration-300">
                
                {/* HEADER */}
                <div className="flex items-start gap-4">
                    {!isSidebarOpen && (
                        <button 
                            onClick={() => setIsSidebarOpen(true)}
                            className="p-2 mt-1 bg-[#111c44] border border-slate-800 rounded-xl hover:bg-slate-800 text-blue-500 transition font-bold text-lg"
                            title="Buka Sidebar"
                        >
                            ☰
                        </button>
                    )}
                    <div className="flex-1">
                        <DashboardHeader device={device} setDevice={setDevice} latestTime={latest.created_at} />
                    </div>
                </div>

                {/* METRICS ROW */}
                <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-8">
                    <MetricCard title="Voltage (Avg)" value={latest.ua} unit="V" />
                    <MetricCard title="Current (Avg)" value={latest.ia} unit="A" />
                    <MetricCard title="Active Power (Total)" value={latest.pt ? (latest.pt / 1000).toFixed(1) : undefined} unit="kW" />
                    <MetricCard title="Frequency" value={latest.freq} unit="Hz" />
                </section>

                {/* ACCORDION GRAPHS SECTION */}
                <div className="space-y-4">
                    
                    {/* ================= GROUP 1: VOLTAGE & CURRENT ================= */}
                    <div className="border border-slate-800 rounded-2xl bg-[#111c44]/30 overflow-hidden">
                        <button
                            onClick={() => setIsVoltageCurrentOpen(!isVoltageCurrentOpen)}
                            className="w-full flex items-center justify-between p-4 bg-[#111c44] hover:bg-[#162256] transition text-left font-medium text-slate-200"
                        >
                            <div className="flex items-center gap-3">
                                <span className={`text-xs transition-transform duration-200 ${isVoltageCurrentOpen ? "rotate-90 text-cyan-400" : "text-slate-500"}`}>
                                    ▶
                                </span>
                                <span className="text-sm font-semibold tracking-wide">Voltage & Current</span>
                            </div>
                            <span className="text-xs text-slate-400 bg-slate-800/80 px-2.5 py-0.5 rounded-full border border-slate-700">
                                {isVoltageCurrentOpen ? "Hide" : "Show"}
                            </span>
                        </button>

                        {isVoltageCurrentOpen && (
                            <div className="p-5 grid grid-cols-1 lg:grid-cols-2 gap-6 bg-[#070d1e]/40 border-t border-slate-800/50">
                                <div className="bg-[#111c44] p-5 rounded-3xl border border-slate-800 flex flex-col justify-between">
                                    <div className="flex items-center justify-between mb-4 flex-wrap gap-2">
                                        <h3 className="text-sm font-bold uppercase tracking-wider text-blue-400 flex items-center gap-2">
                                            <span>⚡</span> 1. Voltage Parameters
                                        </h3>
                                        <MultiSelect options={["ua", "ub", "uc", "uab", "ubc", "uca"]} selected={voltageSelected} setSelected={setVoltageSelected} />
                                    </div>
                                    <ChartCard title="" data={data} selected={voltageSelected} />
                                </div>

                                <div className="bg-[#111c44] p-5 rounded-3xl border border-slate-800 flex flex-col justify-between">
                                    <div className="flex items-center justify-between mb-4 flex-wrap gap-2">
                                        <h3 className="text-sm font-bold uppercase tracking-wider text-emerald-400 flex items-center gap-2">
                                            <span>🔌</span> 2. Current Parameters
                                        </h3>
                                        <MultiSelect options={["ia", "ib", "ic"]} selected={currentSelected} setSelected={setCurrentSelected} />
                                    </div>
                                    <ChartCard title="" data={data} selected={currentSelected} />
                                </div>
                            </div>
                        )}
                    </div>

                    {/* ================= GROUP 2: POWER & ENERGY ================= */}
                    <div className="border border-slate-800 rounded-2xl bg-[#111c44]/30 overflow-hidden">
                        <button
                            onClick={() => setIsPowerEnergyOpen(!isPowerEnergyOpen)}
                            className="w-full flex items-center justify-between p-4 bg-[#111c44] hover:bg-[#162256] transition text-left font-medium text-slate-200"
                        >
                            <div className="flex items-center gap-3">
                                <span className={`text-xs transition-transform duration-200 ${isPowerEnergyOpen ? "rotate-90 text-cyan-400" : "text-slate-500"}`}>
                                    ▶
                                </span>
                                <span className="text-sm font-semibold tracking-wide">Power & Energy</span>
                            </div>
                            <span className="text-xs text-slate-400 bg-slate-800/80 px-2.5 py-0.5 rounded-full border border-slate-700">
                                {isPowerEnergyOpen ? "Hide" : "Show"}
                            </span>
                        </button>

                        {isPowerEnergyOpen && (
                            <div className="p-5 grid grid-cols-1 lg:grid-cols-2 gap-6 bg-[#070d1e]/40 border-t border-slate-800/50">
                                <div className="bg-[#111c44] p-5 rounded-3xl border border-slate-800 flex flex-col justify-between">
                                    <div className="flex items-center justify-between mb-4 flex-wrap gap-2">
                                        <h3 className="text-sm font-bold uppercase tracking-wider text-orange-400 flex items-center gap-2">
                                            <span>🔥</span> 3. Active Power
                                        </h3>
                                        <MultiSelect options={["pt", "pa", "pb", "pc"]} selected={powerSelected} setSelected={setPowerSelected} />
                                    </div>
                                    <ChartCard title="" data={data} selected={powerSelected} />
                                </div>

                                <div className="bg-[#111c44] p-5 rounded-3xl border border-slate-800 flex flex-col justify-between">
                                    <div className="flex items-center justify-between mb-4 flex-wrap gap-2">
                                        <h3 className="text-sm font-bold uppercase tracking-wider text-purple-400 flex items-center gap-2">
                                            <span>🔋</span> 4. Energy Parameters
                                        </h3>
                                        <MultiSelect options={["impep", "expep", "q1eq"]} selected={energySelected} setSelected={setEnergySelected} />
                                    </div>
                                    <ChartCard title="" data={data} selected={energySelected} />
                                </div>
                            </div>
                        )}
                    </div>

                    {/* ================= GROUP 3: DATA PEAK (TABEL data_peak) ================= */}
                    <div className="border border-slate-800 rounded-2xl bg-[#111c44]/30 overflow-hidden">
                        <button
                            onClick={() => setIsDataPeakOpen(!isDataPeakOpen)}
                            className="w-full flex items-center justify-between p-4 bg-[#111c44] hover:bg-[#162256] transition text-left font-medium text-slate-200"
                        >
                            <div className="flex items-center gap-3">
                                <span className={`text-xs transition-transform duration-200 ${isDataPeakOpen ? "rotate-90 text-cyan-400" : "text-slate-500"}`}>
                                    ▶
                                </span>
                                <span className="text-sm font-semibold tracking-wide">Data Peak</span>
                            </div>
                            <span className="text-xs text-slate-400 bg-slate-800/80 px-2.5 py-0.5 rounded-full border border-slate-700">
                                {isDataPeakOpen ? "Hide" : "Show"}
                            </span>
                        </button>

                        {isDataPeakOpen && (
                            <div className="p-5 grid grid-cols-1 gap-6 bg-[#070d1e]/40 border-t border-slate-800/50">
                                <div className="bg-[#111c44] p-5 rounded-3xl border border-slate-800 flex flex-col justify-between">
                                    <div className="flex items-center justify-between mb-4 flex-wrap gap-2">
                                        <h3 className="text-sm font-bold uppercase tracking-wider text-cyan-400 flex items-center gap-2">
                                            <span>📈</span> 5. Data Peak Parameters
                                        </h3>
                                        <MultiSelect 
                                            options={["uab", "ua", "q4eq", "pfc", "q1eq", "pft", "pfa", "ia", "ic", "pt", "pa", "pb", "qt", "qa", "qb", "qc", "pc"]} 
                                            selected={dataPeakSelected} 
                                            setSelected={setDataPeakSelected} 
                                        />
                                    </div>
                                    {/* 5. DATA INPUT MENGGUNAKAN dataPeak BUKAN data UTAMA */}
                                    <ChartCard title="" data={dataPeak} selected={dataPeakSelected} />
                                </div>
                            </div>
                        )}
                    </div>

                </div>
            </main>
        </div>
    );
}