import React from 'react';
import './Logs.css';

function Logs() {
  const logs = [
    { type: 'Error', level: 'Error', message: 'Failed to fetch data', timestamp: '2023-07-01 11:30' },
    { type: 'Info', level: 'Error', message: 'Data updated successfully', timestamp: '2023-05-28 11:23' },
    { type: 'Info', level: 'Info', message: 'User login attempt', timestamp: '2022-02-08 11:22' },
    { type: 'Info', level: 'Info', message: 'Error processing request', timestamp: '2023-02-08 11:27' },
    { type: 'Info', level: 'Info', message: 'Error processing request', timestamp: '2023-02-08 11:38' },
  ];

  return (
    <div className="logs-page">
      <div className="logs-panel">
        <div className="logs-table">
          <table>
            <thead>
              <tr>
                <th>Type</th>
                <th>Level</th>
                <th>Message</th>
                <th>Timestamp</th>
              </tr>
            </thead>
            <tbody>
              {logs.map((log, index) => (
                <tr key={index}>
                  <td>
                    <span className={`log-type ${log.type.toLowerCase()}`}>
                      {log.type}
                    </span>
                  </td>
                  <td>{log.level}</td>
                  <td>{log.message}</td>
                  <td>{log.timestamp}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Logs;
