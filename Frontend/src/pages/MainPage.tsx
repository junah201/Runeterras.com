import React from "react";
import styled from "styled-components";
import { Link } from "react-router-dom";

import Deck from "../components/deck/Deck";
import { DeckInfo } from "../types/deck";

const StyledMainPage = styled.main`
	margin: 60px 0;
`;

const StyledIntroductionContainer = styled.div`
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;

	& h1 {
		color: #ffffff;
		font-size: 40px;
		font-weight: bold;
	}

	& p {
		color: #ffffff;
		font-size: 20px;
	}
`;

const StyledDeckContainer = styled.div`
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
`;

const StyledMoreDeckLink = styled(Link)`
	background-color: #262161;
	color: #ffffff;
	padding: 12px 0;
	max-width: 1250px;
	min-width: 1250px;
	border-radius: 10px;

	display: flex;
	align-items: center;
	justify-content: center;
	text-decoration: none;
`;

const MainPage: React.FC = () => {
	const [totalMasterUserCount, setTotalMasterUserCount] = React.useState(0);
	const [totalMatchDataCount, setTotalMatchDataCount] = React.useState(0);
	const [lastUpdatedAt, setLastUpdatedAt] = React.useState("12 Hours ago");
	const [deckList, setDeckList] = React.useState<DeckInfo[]>([]);

	const domeDeck: DeckInfo = {
		id: 1,
		pickRate: 0.1,
		winRate: 0.2,
		factions: ["bandle_city", "bilgewater"],
		champions: ["jayce", "jayce"],
		cards: [1, 2, 3, 4, 5, 6, 7, 8].map((id) => {
			return {
				id: id,
				name: "jayce",
				filename: "jayce",
			};
		}),
	};

	React.useEffect(() => {
		setDeckList([domeDeck, domeDeck, domeDeck]);
	}, []);

	return (
		<StyledMainPage>
			<StyledIntroductionContainer>
				<h1>룬테라 덱 통계 분석 프로젝트</h1>
				<p>
					Runeterras.com은 Riot의 Regends of Runeterra의 덱들의 통계를 분석하는
					프로젝트입니다.
				</p>
				<p>
					현재 {totalMasterUserCount}명의 마스터 유저들로부터{" "}
					{totalMatchDataCount}개의 매치 데이터를 수집하여 통계를 분석하고
					있습니다.
				</p>
			</StyledIntroductionContainer>
			<StyledDeckContainer>
				{deckList.map((deck) => (
					<Deck key={deck.id} deck={deck} />
				))}
				<StyledMoreDeckLink to="/deck/meta">전체 목록 보기</StyledMoreDeckLink>
			</StyledDeckContainer>
		</StyledMainPage>
	);
};

export default MainPage;
