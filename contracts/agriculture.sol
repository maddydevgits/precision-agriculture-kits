// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract agriculture {

  string[] _usernames;
  string[] _passwords;

  
  mapping(string=>bool) _registeredUsers;

  constructor() {
  }

  function addUser(string memory username,string memory password) public {
    require(!_registeredUsers[username]);

    _usernames.push(username);
    _passwords.push(password);
    _registeredUsers[username]=true;
  }

  function viewUsers() public view returns(string[] memory,string[] memory) {
    return (_usernames,_passwords);
  }

  function precisionForSoilMoisture(uint value) public pure returns(uint) {
    if(value>1000 && value<1024) {
      return 1;
    } else if(value>800 && value<1000){
      return 2;
    } else if(value>600 && value<800) {
      return 3;
    } else if(value>400 && value<600) {
      return 4;
    } else {
      return 5;
    }
  }

  function precisionForLightIntensity(uint value) public pure returns(uint){
    if(value<5){
      return 1;
    } else if(value>5 && value<10){
      return 2;
    } else if(value>10 && value<16){
      return 3;
    } else if(value>16) {
      return 4;
    } else {
      return 5;
    }
  }

  function precisionForHumidity(uint value) public pure returns(uint){
    if(value<50){
      return 1;
    } else if(value>50 && value<60){
      return 2;
    } else if(value>60){
      return 3;
    } else{
      return 4;
    }
  }

  function precisionForRainfall(uint value) public pure returns(uint){
    if(value>800 && value<1024){
      return 1;
    } else if(value>600 && value<800){
      return 2;
    } else if(value>340 && value<600){
      return 3;
    } else {
      return 4;
    }
  }

  function precisionForTemperature(uint value) public pure returns(uint){
    if(value<10){
      return 1;
    } else if(value>10 && value<20){
      return 2;
    } else if(value>20 && value<30){
      return 3;
    } else if(value>30 && value<35){
      return 4;
    } else if(value>35){
      return 5;
    } else {
      return 6;
    }
  }

}
