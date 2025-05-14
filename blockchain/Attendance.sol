// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Attendance {
    struct AttendanceRecord {
        string name;
        uint256 timestamp;
        string hashId;
    }
    
    AttendanceRecord[] public attendanceRecords;
    
    event AttendanceMarked(string name, uint256 timestamp, string hashId);
    
    function markAttendance(string memory name, string memory hashId) public {
        uint256 timestamp = block.timestamp;
        attendanceRecords.push(AttendanceRecord(name, timestamp, hashId));
        emit AttendanceMarked(name, timestamp, hashId);
    }
    
    function getAttendanceCount() public view returns (uint256) {
        return attendanceRecords.length;
    }
    
    function getAttendance(uint256 index) public view returns (string memory, uint256, string memory) {
        require(index < attendanceRecords.length, "Index out of bounds");
        AttendanceRecord memory record = attendanceRecords[index];
        return (record.name, record.timestamp, record.hashId);
    }
} 