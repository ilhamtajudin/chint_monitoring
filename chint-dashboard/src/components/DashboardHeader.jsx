import DeviceSelector from "./DeviceSelector";

export default function DashboardHeader({ device, setDevice, latestTime }) {
    return (
        <header className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8 border-b border-slate-800 pb-5">
            <div>
                <h1 className="text-2xl font-bold tracking-tight">Dashboard</h1>
                <p className="text-sm text-slate-400">Real-time Energy Monitoring System</p>
            </div>
            
            <div className="flex flex-wrap items-center gap-4 bg-[#111c44] p-2 rounded-2xl border border-slate-800">
                <div className="flex flex-col px-2">
                    <span className="text-[10px] font-bold uppercase text-slate-400 mb-0.5">Pilih Device</span>
                    
                    {/* UBAH BAGIAN INI: Sesuaikan nama props dengan yang ada di DeviceSelector.jsx */}
                    <DeviceSelector device={device} setDevice={setDevice} />
                    
                </div>
                <div className="h-8 w-px bg-slate-800 hidden sm:block"></div>
                <div className="flex flex-col px-2">
                    <span className="text-[10px] font-bold uppercase text-slate-400 mb-0.5">Last Update</span>
                    <span className="text-sm font-semibold text-emerald-400">{latestTime || "--:--:--"}</span>
                </div>
            </div>
        </header>
    );
}