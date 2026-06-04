export default function MetricCard({ title, value, unit }) {
  return (
    <div className="bg-slate-800 rounded-2xl p-5 shadow-lg border border-slate-700">
      <h3 className="text-slate-400 text-sm mb-2">{title}</h3>

      <div className="flex items-end gap-2">
        <div className="text-3xl font-bold text-cyan-400">
          {value}
        </div>

        <div className="text-slate-300 text-sm mb-1">
          {unit}
        </div>
      </div>
    </div>
  );
}