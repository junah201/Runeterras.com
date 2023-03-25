import React from "react";
import styled from "styled-components";
import { Link } from "react-router-dom";

import Deck from "../components/deck/Deck";
import { IDeckInfo } from "../types/deck";

import axios from "axios";

import { getDeckFromCode } from "lor-deckcodes-ts";

import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
dayjs.extend(relativeTime);

const StyledMainPage = styled.main`
	margin: 60px 0;
`;

const StyledIntroductionContainer = styled.div`
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 20px;

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

const StyledDeckListInfo = styled.div`
	width: 1250px;
	display: flex;
	flex-direction: row;
	align-items: center;
	justify-content: space-between;

	& p {
		color: #ffffff;
	}
`;

const MetaDecksPage: React.FC = () => {
	const [totalMatchDataCount, setTotalMatchDataCount] = React.useState(0);
	const [lastGamaVersion, setLastGamaVersion] = React.useState(
		"live-green-4-02-32 "
	);
	const [lastUpdatedAt, setLastUpdatedAt] = React.useState("12 Hours ago");
	const [deckList, setDeckList] = React.useState<IDeckInfo[]>([]);

	React.useEffect(() => {
		axios({
			url: `${process.env.REACT_APP_API_URL}/game_version/lastest`,
			method: "GET",
			headers: {
				"Content-Type": "application/json",
				Accept: "application/json",
			},
		}).then((res) => {
			if (res.status === 200) {
				setLastGamaVersion(res.data.game_version);
				setLastUpdatedAt(dayjs(res.data.updated_at).fromNow());
				setTotalMatchDataCount(res.data.total_match_count);
			}
		});
	}, []);

	React.useEffect(() => {
		axios({
			url: `${process.env.REACT_APP_API_URL}/deck/meta/all`,
			params: { limit: 10, skip: 0 },
			method: "GET",
			headers: {
				"Content-Type": "application/json",
				Accept: "application/json",
			},
		}).then((res) => {
			if (res.status === 200) {
				const newDeckList = [];
				for (const deck of res.data) {
					const decodedDeck = getDeckFromCode(deck.deck_code);
					const newDeck: IDeckInfo = {
						id: deck.id,
						totalMatchCount: deck.win_count + deck.lose_count,
						winRate: (
							(deck.win_count * 100) /
							(deck.win_count + deck.lose_count)
						).toFixed(2),
						winCount: deck.win_count,
						loseCount: deck.lose_count,
						firstStartWinCount: deck.first_start_win_count,
						firstStartLoseCount: deck.first_start_lose_count,
						factions: [],
						champions: [],
					};
					for (const card of decodedDeck) {
						newDeck.champions.push(card.cardCode);
					}
					newDeck.factions = [
						...new Set(
							decodedDeck.map((card) => `${card.cardCode.slice(2, 4)}`)
						),
					];
					newDeck.champions = decodedDeck.map((card) => card.cardCode);
					newDeckList.push(newDeck);
				}
				setDeckList(newDeckList);
			}
		});
	}, []);

	return (
		<StyledMainPage>
			<StyledIntroductionContainer>
				<h1>Meta Decks</h1>
			</StyledIntroductionContainer>
			<StyledDeckContainer>
				<StyledDeckListInfo>
					<p>Version : {lastGamaVersion}</p>
					<p>Last Updated : {lastUpdatedAt}</p>
				</StyledDeckListInfo>
				{deckList.map((deck) => (
					<Deck key={deck.id} deck={deck} />
				))}
				<StyledMoreDeckLink to="/deck/meta">더 보기</StyledMoreDeckLink>
			</StyledDeckContainer>
		</StyledMainPage>
	);
};

export default MetaDecksPage;
