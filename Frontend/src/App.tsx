import React from "react";
import { Switch, Route } from "react-router-dom";

import Header from "./components/base/Header";
import Footer from "./components/base/Footer";

import MainPage from "./pages/MainPage";

const App: React.FC = () => {
	return (
		<div className="App">
			<Header />
			<Switch>
				<Route path="/" component={MainPage} />
			</Switch>
			<Footer />
		</div>
	);
};

export default App;
