import React from "react";
import { IDeckCompareDetailInfo } from "../../types/deck";
import styled from "styled-components";
import Card from "../card/Card";
import { getDeckFromCode } from "lor-deckcodes-ts";
import CompareDetail from "./CompareDetail";

const StyledCompareDeck = styled.div`
	display: flex;
	flex-direction: column;
	align-items: center;
	background-color: #262161;
	color: #ffffff;
	padding: 20px;
	border-radius: 10px;
	width: min(1250px, 80vw);

	& + & {
		margin-top: 50px;
	}
`;

const StyledCompareDeckPreview = styled.div`
	display: flex;
	flex-direction: row;
	align-items: center;
	justify-content: space-evenly;
	width: 100%;
	height: 200px;
`;

const StyledCardsContainer = styled.div`
	display: flex;
	flex-direction: row;
	align-items: center;
	justify-content: center;
`;

const StyledDeckVsSpan = styled.span`
	font-size: 1.5rem;
	font-weight: bold;
	margin: 0 20px;
	display: flex;
	text-align: center;
	justify-content: center;
	align-items: center;
	height: 100%;
`;

const StyledDetailButton = styled.button`
	width: 30px;
	height: 30px;
	border: none;
	background-color: #262161;
	margin: 0 30px;

	& img {
		height: 100%;
		width: 100%;
		object-fit: cover;
		filter: invert(78%) sepia(96%) saturate(1878%) hue-rotate(323deg)
			brightness(96%) contrast(99%);
	}
`;

const StyledDeckDivider = styled.div`
	width: 1px;
	height: 180px;
	margin: 0 5px;
	background-color: #534ac1;
`;

const StyledDeckInfo = styled.div`
	display: flex;

	& + & {
		margin-top: 20px;
	}
`;

const CompareDeck: React.FC<{
	data: IDeckCompareDetailInfo;
}> = ({ data }) => {
	console.log(data);
	const [isDetailOpen, setIsDetailOpen] = React.useState(false);
	const myDeck = getDeckFromCode(data.my_deck.deck_code);
	const opponentDeck = getDeckFromCode(data.opponent_deck.deck_code);

	return (
		<StyledCompareDeck>
			<StyledCompareDeckPreview>
				<StyledCardsContainer>
					{myDeck.map((card) => {
						return <Card key={card.cardCode} id={card.cardCode} />;
					})}
				</StyledCardsContainer>
				<StyledDeckVsSpan>VS</StyledDeckVsSpan>
				<StyledCardsContainer>
					{opponentDeck.map((card) => {
						return <Card key={card.cardCode} id={card.cardCode} />;
					})}
				</StyledCardsContainer>
				<StyledDeckDivider />
				<StyledDeckInfo>
					<span>Total {data.win_count + data.lose_count} Matches</span>
				</StyledDeckInfo>
				<StyledDetailButton
					onClick={() => {
						setIsDetailOpen((prev) => {
							return !prev;
						});
					}}
				>
					<img src="/arrow_down.svg" alt="arrow_down" />
				</StyledDetailButton>
			</StyledCompareDeckPreview>{" "}
			{isDetailOpen && (
				<CompareDetail
					data={data}
					myDeck={myDeck}
					opponentDeck={opponentDeck}
				/>
			)}
		</StyledCompareDeck>
	);
};

export default CompareDeck;
