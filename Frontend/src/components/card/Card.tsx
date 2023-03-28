import React from "react";
import styled from "styled-components";

const StyledCard = styled.div`
	overflow: hidden;

	max-height: 150px;
	max-width: 100px;

	& + & {
		margin-left: 8px;
	}

	& img {
		height: 100%;
		width: 100%;
		object-fit: cover;
	}

	&:hover {
		transform: scale(1.1);
		transition: transform 0.5s;
	}
`;

const Card: React.FC<{
	id: string;
}> = ({ id }) => {
	return (
		<StyledCard key={id}>
			<img
				src={`${process.env.REACT_APP_CDN_URL}/images/card/ko/${id}.png`}
				alt={id}
			/>
		</StyledCard>
	);
};

export default Card;
