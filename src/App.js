import "./App.css";
import React from "react";
import PredictsList from "./components/PredictsList";
import {Route,Routes} from 'react-router-dom';
import PredictsPage from './pages/PredictPage';

function App() {
  return (
  	<Routes>
		<Route path="/" element={<PredictsPage/>} />
		<Route path="/:pk" element={<PredictsPage />} />
	</Routes>
  );
};

export default App;
