import React from "react";
import styled from "styled-components";
import { getDeckFromCode } from "lor-deckcodes-ts";

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
	}

	& button {
		margin: 6px;
		background: inherit;
		border: none;
		color: #ffffff;
		padding: 4px;
		border-radius: 4px;
		border: 1px solid #534ac1;
	}
`;

const StyledDeckCardPreview = styled.div`
	display: grid;
	grid-template-columns: repeat(8, 1fr);
	grid-template-rows: repeat(2, 1fr);

	& div {
		display: flex;
		overflow: hidden;
		height: 120px;
		width: 80px;

		& img {
			width: 100%;
			height: 100%;
			object-fit: cover;
		}
	}
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
					return (
						<div key={card.cardCode}>
							<img
								src={`${process.env.REACT_APP_CDN_URL}/images/card/ko/${card.cardCode}.png`}
								alt={card.cardCode}
							/>
						</div>
					);
				})}
			</StyledDeckCardPreview>
		</StyledDeck>
	);
};

export default DeckCode;
