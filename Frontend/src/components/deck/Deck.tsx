import styled from "styled-components";

import { DeckInfo } from "../../types/deck";

const StyledDeck = styled.div`
	display: flex;
	flex-direction: row;
	align-items: center;
	justify-content: center;

	padding: 10px 40px;
	background-color: #262161;
	border-radius: 10px;

	max-width: 1250px;
	min-width: 1250px;
	height: 200px;
	margin: 12px 0;
`;

const StyledDeckInfoContainer = styled.div`
	display: flex;
	flex-direction: column;
`;

const StyledDeckInfoWrapper = styled.div`
	display: flex;

	& + & {
		margin-top: 20px;
	}
`;

const StyledDeckRateInfo = styled.div`
	display: flex;
	flex-direction: column;

	color: #ffffff;
`;

const StyledFactionContainer = styled.div`
	display: flex;
	flex-direction: row;
	margin-right: 20px;

	& div {
		height: 32px;
		width: 32px;

		& img {
			height: 100%;
			width: 100%;
			object-fit: cover;
		}
	}

	& div + div {
		margin-left: 24px;
	}
`;

const StyledChampionContainer = styled.div`
	display: flex;
	flex-direction: row;
	align-items: center;
	justify-content: center;

	color: #ffffff;
	font-size: 16px;
	font-weight: bold;

	& div + div {
		margin-left: 12px;
	}
`;

const StyledDeckDivider = styled.div`
	width: 1px;
	height: 180px;
	background-color: #534ac1;
	margin: 0 50px;
`;

const StyledCardsContainer = styled.div`
	display: flex;
`;

const StyledCard = styled.div`
	overflow: hidden;

	height: 150px;
	width: 100px;

	& + & {
		margin-left: 8px;
	}

	& img {
		height: 100%;
		width: 100%;
		object-fit: cover;
	}
`;

const Deck: React.FC<{ deck: DeckInfo }> = (props) => {
	console.log(process.env.REACT_APP_CDN_URL);

	return (
		<StyledDeck key={props.deck.id}>
			<StyledDeckInfoContainer>
				<StyledDeckInfoWrapper>
					<StyledFactionContainer>
						{props.deck.factions.map((faction) => {
							return (
								<div>
									<img
										src={`${process.env.REACT_APP_CDN_URL}/images/faction/${faction}.svg`}
										alt={faction}
									/>
								</div>
							);
						})}
					</StyledFactionContainer>
					<StyledChampionContainer>
						{props.deck.champions.map((champion) => {
							return <div>{champion}</div>;
						})}
					</StyledChampionContainer>
				</StyledDeckInfoWrapper>
				<StyledDeckInfoWrapper>
					<StyledDeckRateInfo>
						<span>Pick Rate : {props.deck.pickRate}%</span>
						<span>Win Rate : {props.deck.winRate}%</span>
					</StyledDeckRateInfo>
				</StyledDeckInfoWrapper>
			</StyledDeckInfoContainer>
			<StyledDeckDivider />
			<StyledCardsContainer>
				{props.deck.cards.map((card) => {
					return (
						<StyledCard>
							<img
								src={`${process.env.REACT_APP_CDN_URL}/images/card/${card.filename}.png`}
								alt={card.name}
							/>
						</StyledCard>
					);
				})}
			</StyledCardsContainer>
		</StyledDeck>
	);
};

export default Deck;
