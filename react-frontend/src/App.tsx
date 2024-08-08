// src/App.tsx

import React, { useEffect, useState } from 'react';
import axios from 'axios';
// Axios is a promise based http client that will be used to fetch data using our API


interface Device {
  ip: string;
  mac: string;
  hostname: string;
  status: string;
  open_ports: string;
  services: string;
  traffic_bytes: number;
  traffic_packets: number;
}

const App: React.FC = () => {
  const [devices, setDevices] = useState<Device[]>([]);

  useEffect(() => {
    // Fetch devices from the backend
    // Axios makes the request, the then method takes the response and runs the setDevices() method.
    axios.get<Device[]>('http://localhost:5000/devices')
        .then(response => {
          console.log('Fetched devices:', response.data);
          setDevices(response.data);
        })
        .catch(error => {
          console.error('Error fetching devices:', error);
        });
  }, []);

  return (
      <div className="App">
        <h1>Network Devices</h1>
        <table>
          <thead>
          <tr>
            <th>IP Address</th>
            <th>MAC Address</th>
            <th>Hostname</th>
            <th>Status</th>
            <th>Open Ports</th>
            <th>Services</th>
            <th>Traffic (Bytes)</th>
            <th>Traffic (Packets)</th>
          </tr>
          </thead>
          <tbody>
          {devices.map((device, index) => (
              <tr key={index}>
                <td>{device.ip}</td>
                <td>{device.mac}</td>
                <td>{device.hostname}</td>
                <td>{device.status}</td>
                <td>{device.open_ports}</td>
                <td>{device.services}</td>
                <td>{device.traffic_bytes}</td>
                <td>{device.traffic_packets}</td>
              </tr>
          ))}
          </tbody>
        </table>
      </div>
  );
};

export default App;
