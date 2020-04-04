import React, { Component } from "react";
import logo from "../logo.svg";
import { Link } from "react-router-dom";
import "../stylesheets/Header.css";

class Header extends Component {
  render() {
    return (
      <div className="App-header">
        <h1>
          <Link to="/">Udacitrivia</Link>
        </h1>
        <h2>
          <Link to="/">List</Link>
        </h2>
        <h2>
          <Link to="/add">Add</Link>
        </h2>
        <h2>
          <Link to="/play">Play</Link>
        </h2>
      </div>
    );
  }
}

export default Header;
