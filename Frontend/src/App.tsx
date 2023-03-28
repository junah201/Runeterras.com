import React from "react";
import { Switch, Route } from "react-router-dom";

import Header from "./components/base/Header";
import Footer from "./components/base/Footer";

import MainPage from "./pages/MainPage";
import MetaDecksPage from "./pages/MetaDecksPage";
import MetaDeckComparePage from "./pages/MetaDeckComparePage";
import NotFoundPage from "./pages/NotFoundPage";

const App: React.FC = () => {
	return (
		<div className="App">
			<Header />
			<Switch>
				<Route exact path="/">
					<MainPage />
				</Route>
				<Route exact path="/deck/meta">
					<MetaDecksPage />
				</Route>
				<Route exact path="/deck/compare">
					<MetaDeckComparePage />
				</Route>
				<Route path="*">
					<NotFoundPage />
				</Route>
			</Switch>
			<Footer />
		</div>
	);
};

export default App;
