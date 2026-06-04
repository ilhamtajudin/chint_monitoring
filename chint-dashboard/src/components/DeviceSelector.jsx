export default function DeviceSelector({
  device,
  setDevice,
}) {
  return (
    <div className="flex gap-4 mb-6">
      <button
        onClick={() => setDevice("chint_1")}
        className={`px-5 py-3 rounded-xl
        ${
          device === "chint_1"
            ? "bg-cyan-500"
            : "bg-slate-700"
        }`}
      >
        CHINT_1
      </button>

      <button
        onClick={() => setDevice("chint_2")}
        className={`px-5 py-3 rounded-xl
        ${
          device === "chint_2"
            ? "bg-cyan-500"
            : "bg-slate-700"
        }`}
      >
        CHINT_2
      </button>
    </div>
  );
}