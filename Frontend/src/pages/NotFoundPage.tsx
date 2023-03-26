import React from "react";
import styled from "styled-components";

const StyledNotFoundPage = styled.main`
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	width: 100%;
	height: 100%;
	padding: 20px;

	& span {
		font-size: 20px;
		font-weight: bold;
		color: #ffffff;
	}
`;

const NotFoundPage: React.FC = () => {
	return (
		<StyledNotFoundPage>
			<span>404 Page Not Found</span>
		</StyledNotFoundPage>
	);
};

export default NotFoundPage;
