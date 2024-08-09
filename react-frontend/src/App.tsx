// src/App.tsx

import Home from './components/home';
import NetworkTopology from './components/topology';
// our components for corresponding pages in our app
import React, { useEffect, useState } from 'react';
import axios from 'axios';
// Axios is a promise based http client that will be used to fetch data using our API
import { Tooltip } from 'react-tooltip';
import 'react-tooltip/dist/react-tooltip.css';
// tool tip functionality
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
// routing solution since we're not using next.js

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
  const [visibleDevices, setVisibleDevices] = useState(8);
  // The visible devices is the starting amount of devices displayed on the homescreen

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

  // Function that renders additional devices.
  const loadMoreDevices = () => {
      setVisibleDevices(prevVisibleDevices => prevVisibleDevices + 8);
  };

  //Function that returns human readable bytes.
  const humanBytes = (bytes:number) => {
      if(bytes > 1_000_000_000)
          return (bytes/1_000_000_000).toFixed(2) + 'gb'
      if(bytes > 1_000_000)
          return (bytes/1_000_000).toFixed(2) + 'mb'
      if(bytes > 1_000)
          return (bytes/1_000).toFixed(2) + 'kb'
      return bytes + ''
  }

  // Helper function to split apart data in some of the device data fields
  const formatTooltipContent = (content: string) => {
      return content.split(',').map((item, index) => <div key={index}>{item.trim()}</div>);
  };

  return (
      <Router>
          <Routes>
              <Route
                  path="/"
                  element={<Home
                      devices={devices}
                      visibleDevices={visibleDevices}
                      loadMoreDevices={loadMoreDevices}
                      humanBytes={humanBytes}
                      formatTooltipContent={formatTooltipContent}
                  />}
              />
              <Route path="/topology" element={<NetworkTopology />} />
          </Routes>
      </Router>
  );
};

export default App;
