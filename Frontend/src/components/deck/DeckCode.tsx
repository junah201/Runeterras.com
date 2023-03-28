import React from "react";
import styled from "styled-components";
import { getDeckFromCode } from "lor-deckcodes-ts";
import Card from "../card/Card";

const StyledDeck = styled.div`
	display: flex;
	flex-direction: row;
	align-items: center;
	justify-content: space-evenly;
	background-color: #262161;
	border-radius: 8px;
	border: 1px solid #534ac1;
	padding: 10px;

	& + & {
		margin-top: 16px;
	}
`;

const StyledDeckInfoPreview = styled.div`
	display: flex;
	flex-direction: column;
	align-items: center;

	color: #ffffff;

	& p {
		margin: 6px;
		font-size: 1rem;
	}

	& button {
		margin: 6px;
		background: inherit;
		border: none;
		color: #ffffff;
		padding: 4px;
		font-size: 1rem;
		border-radius: 4px;
		border: 1px solid #534ac1;
	}
`;

const StyledDeckCardPreview = styled.div`
	display: grid;
	grid-template-columns: repeat(8, 1fr);
	grid-template-rows: repeat(2, 1fr);
`;

const DeckCode: React.FC<{
	code: string;
	win_count: number;
	lose_count: number;
}> = (props) => {
	const cards = getDeckFromCode(props.code);

	return (
		<StyledDeck>
			<StyledDeckInfoPreview>
				<p>Win : {props.win_count}</p>
				<p>Lose : {props.lose_count}</p>
				<button
					onClick={() => {
						navigator.clipboard.writeText(props.code);
					}}
				>
					Copy Deck Code
				</button>
			</StyledDeckInfoPreview>
			<StyledDeckCardPreview>
				{cards.map((card) => {
					return <Card key={card.cardCode} id={card.cardCode} />;
				})}
			</StyledDeckCardPreview>
		</StyledDeck>
	);
};

export default DeckCode;
