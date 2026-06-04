export default function Sidebar({ currentDevice, isOpen, setIsOpen }) {
    return (
        <aside 
            className={`bg-[#111c44] border-r border-slate-800 p-5 flex flex-col justify-between transition-all duration-300 ease-in-out h-screen sticky top-0
                ${isOpen ? "w-64 opacity-100" : "w-0 p-0 opacity-0 overflow-hidden border-none"}`}
        >
            <div>
                {/* LOGO & TOGGLE BUTTON */}
                <div className="flex items-center justify-between mb-8 px-2 whitespace-nowrap">
                    <div className="flex items-center gap-3">
                        <div className="font-bold text-xl tracking-wider text-blue-500">CHNT</div>
                        <div className="text-xs text-slate-400 self-end pb-0.5">DTSU666 Monitor</div>
                    </div>
                    
                    {/* Tombol sembunyikan sidebar */}
                    <button 
                        onClick={() => setIsOpen(false)}
                        className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800 text-sm transition"
                        title="Sembunyikan Sidebar"
                    >
                        ◀
                    </button>
                </div>

                <nav className="space-y-1 whitespace-nowrap">
                    <a href="#" className="flex items-center gap-3 px-3 py-2.5 bg-blue-600 rounded-xl text-white font-medium">
                        <span>📊</span> Dashboard
                    </a>
                    <a href="#" className="flex items-center gap-3 px-3 py-2.5 text-slate-400 hover:bg-slate-800 rounded-xl transition">
                        <span>⏱️</span> Real-time Monitor
                    </a>
                    <a href="#" className="flex items-center gap-3 px-3 py-2.5 text-slate-400 hover:bg-slate-800 rounded-xl transition">
                        <span>🖥️</span> Devices
                    </a>
                    <a href="#" className="flex items-center gap-3 px-3 py-2.5 text-slate-400 hover:bg-slate-800 rounded-xl transition">
                        <span>📂</span> Historical Data
                    </a>
                </nav>
            </div>
            
            {/* DEVICE STATUS QUICK LIST */}
            <div className="bg-[#1b254b] p-4 rounded-2xl border border-slate-800 whitespace-nowrap">
                <div className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">Device Status</div>
                <div className="space-y-2 text-sm">
                    <div className="flex items-center justify-between">
                        <span className={currentDevice === "chint_1" ? "text-blue-400 font-bold" : "text-slate-300"}>CHINT_1</span>
                        <span className="flex h-2 w-2 rounded-full bg-emerald-500"></span>
                    </div>
                    <div className="flex items-center justify-between">
                        <span className={currentDevice === "chint_2" ? "text-blue-400 font-bold" : "text-slate-300"}>CHINT_2</span>
                        <span className="flex h-2 w-2 rounded-full bg-emerald-500"></span>
                    </div>
                </div>
            </div>
        </aside>
    );
}