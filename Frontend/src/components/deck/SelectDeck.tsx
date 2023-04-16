import React from "react";
import styled from "styled-components";

import { ChampionCard } from "../../types/card";

const StyledSelectDeck = styled.div`
	background-color: #262161;
	width: 100%;
	padding: 20px;

	& + & {
		margin-top: 30px;
	}
`;

const SelectDeck: React.FC<{
	deckChampionCards: ChampionCard[];
	setDeckChampionCards: Function;
	championCards: ChampionCard[];
}> = (props) => {
	const regions = [
		{ name: "bandlecity", code: "BC" },
		{ name: "bilgewater", code: "BW" },
		{ name: "demacia", code: "DE" },
		{ name: "freljord", code: "FR" },
		{ name: "ionia", code: "IO" },
		{ name: "noxus", code: "NX" },
		{ name: "piltoverzaun", code: "PZ" },
		{ name: "runeterra", code: "RU" },
		{ name: "shadowisles", code: "SI" },
		{ name: "shurima", code: "SH" },
		{ name: "targon", code: "MT" },
	];

	const [selectedRegions, setSelectedRegions] = React.useState<string[]>([
		"bandlecity",
	]);

	return (
		<StyledSelectDeck>
			<StyledRegionSelectContainer>
				{regions.map((region) => {
					return (
						<RegionSelect
							region={region}
							key={region.name}
							selectedRegions={selectedRegions}
							setSelectedRegions={setSelectedRegions}
							setSelectedChampions={props.setDeckChampionCards}
						/>
					);
				})}
			</StyledRegionSelectContainer>
			<ChampionSelectContainer>
				{props.championCards
					.filter((championCard) => {
						return selectedRegions.includes(championCard.region);
					})
					.map((championCard) => {
						return (
							<ChampionSelect
								isSelect={props.deckChampionCards
									.map((champion) => champion.id)
									.includes(championCard.id)}
								onClick={() => {
									props.setDeckChampionCards((prev: ChampionCard[]) => {
										if (prev.includes(championCard)) {
											return prev.filter((champion) => {
												return champion.id !== championCard.id;
											});
										}
										if (prev.length >= 3) {
											return prev;
										}
										return [...prev, championCard];
									});
								}}
								key={championCard.id}
							>
								<div>
									<img
										src={`${process.env.REACT_APP_CDN_URL}/images/card/en/${championCard.id}-full.png`}
										alt={championCard.name}
									/>
								</div>
								<span>{championCard.name}</span>
							</ChampionSelect>
						);
					})}
			</ChampionSelectContainer>
		</StyledSelectDeck>
	);
};

const StyledRegionSelectContainer = styled.div`
	display: flex;
`;

const ChampionSelectContainer = styled.div`
	display: grid;
	grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
	grid-gap: 10px;
`;

interface Container {
	isSelect: boolean;
}

const ChampionSelect = styled.div<Container>`
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	width: 100px;
	overflow: hidden;

	filter: ${(props) => (props.isSelect ? "none" : "grayscale(50%)")};

	& div {
		width: 100px;
		height: 100px;

		border: ${(props) => (props.isSelect ? "4.5px solid #fbaf41" : "none")};
		border-radius: 50%;
		overflow: hidden;

		& img {
			width: 100%;
			height: 100%;
			object-fit: cover;
		}
	}

	& span {
		margin-top: 5px;
		color: ${(props) => (props.isSelect ? "#fbaf41" : "#fff")};
		font-weight: ${(props) => (props.isSelect ? "bold" : "normal")};
		text-align: center;
	}
`;

const StyledRegionSelect = styled.div<Container>`
	display: flex;
	align-items: center;
	justify-content: center;
	width: 50px;
	height: 50px;
	overflow: hidden;

	border: ${(props) => (props.isSelect ? "1px solid #fbaf41" : "none")};

	& img {
		padding: 8px;
		width: 100%;
		height: 100%;
		object-fit: cover;
	}
`;

const RegionSelect: React.FC<{
	region: any;
	selectedRegions: string[];
	setSelectedRegions: Function;
	setSelectedChampions: Function;
}> = ({
	region,
	selectedRegions,
	setSelectedRegions,
	setSelectedChampions,
}) => {
	return (
		<StyledRegionSelect
			onClick={() => {
				setSelectedRegions((prev: string[]) => {
					if (prev.includes(region.name)) {
						const newSelectRegions: string[] = prev.filter((regionName) => {
							return regionName !== region.name;
						});
						setSelectedChampions((prev: ChampionCard[]) => {
							return prev.filter((champion) => {
								return champion.region !== region.name;
							});
						});
						return newSelectRegions;
					}
					if (prev.length >= 2) {
						return prev;
					}
					return [...prev, region.name];
				});
			}}
			isSelect={selectedRegions.includes(region.name)}
		>
			<img
				src={`${process.env.REACT_APP_CDN_URL}/images/faction/${region.code}.svg`}
				alt={region.name}
			/>
		</StyledRegionSelect>
	);
};

export default SelectDeck;
