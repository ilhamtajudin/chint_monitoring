import axios from "axios";

const API = axios.create({
    baseURL: "http://192.168.2.201:5000/api",
});

// =====================================================
// GET DATA REALTIME
// =====================================================

export const getDeviceData = async (device) => {
    const res = await API.get(`/${device}`);
    return res.data;
};

// =====================================================
// GET DATA PEAK
// =====================================================

export const getDataPeak = async (device) => {
    const res = await API.get(`/data_peak/${device}`);
    return res.data;
};

// =====================================================
// GET LIST DEVICE
// =====================================================

export const getDevices = async () => {
    const res = await API.get("/devices");
    return res.data;
};