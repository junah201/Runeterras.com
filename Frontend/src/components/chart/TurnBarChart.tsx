import React from "react";
import { ResponsiveBar } from "@nivo/bar";
import styled from "styled-components";

const StyledTurnBarChart = styled.div`
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	width: 100%;
	height: 100%;

	& span {
		font-size: 20px;
		font-weight: bold;
		color: #ffffff;
	}

	& text {
		color: #ffffff;
		fill: #ffffff;
	}
`;

const TurnBarChart: React.FC<{ data: any; keys: string[] }> = (props) => {
	return (
		<StyledTurnBarChart>
			<span>Turn</span>
			<ResponsiveBar
				data={props.data}
				theme={{
					axis: {
						legend: {
							text: { fill: "#ffffff" },
						},
						ticks: {
							line: {
								stroke: "#ffffff",
							},
							text: {
								fill: "#ffffff",
							},
						},
					},
				}}
				keys={props.keys}
				indexBy="turn"
				margin={{ top: 50, right: 70, bottom: 80, left: 60 }}
				padding={0.3}
				valueScale={{ type: "linear" }}
				indexScale={{ type: "band", round: true }}
				colors={{ scheme: "nivo" }}
				borderColor={{
					from: "color",
					modifiers: [["darker", 1.6]],
				}}
				axisTop={null}
				axisRight={null}
				axisBottom={{
					tickSize: 5,
					tickPadding: 5,
					tickRotation: 0,
					legend: "turn",
					legendPosition: "middle",
					legendOffset: 32,
				}}
				animate={false}
				axisLeft={{
					tickSize: 5,
					tickPadding: 5,
					tickRotation: 0,
					legend: "count",
					legendPosition: "middle",
					legendOffset: -40,
				}}
				labelSkipWidth={12}
				labelSkipHeight={12}
				labelTextColor="#ffffff"
				legends={[
					{
						dataFrom: "keys",
						anchor: "right",
						direction: "column",
						justify: false,
						translateX: 120,
						translateY: 0,
						itemsSpacing: 2,
						itemWidth: 100,
						itemHeight: 20,
						itemDirection: "left-to-right",
						itemOpacity: 0.85,
						symbolSize: 20,
						effects: [
							{
								on: "hover",
								style: {
									itemOpacity: 1,
								},
							},
						],
						itemTextColor: "#ffffff",
					},
				]}
				isInteractive={false}
				enableGridY={false}
			/>
		</StyledTurnBarChart>
	);
};

export default TurnBarChart;
