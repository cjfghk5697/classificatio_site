import styled from 'styled-components';

const PredictsItemBlock =styled.div`
	display:flex;
	.thumbnail{
		margin-right: 1rem;
		img{
			display:block;
			width:160px;
			height:100px;
			object-fit:cover;
		}
	}
	.contents{
		h2{
		margin:0;
			a{
				color:black;
			}
		}
		p{
			margin:0;
			line-height:1.5;
			margin-top:0.5rem;
			white-space:normal;
			
		}
	}
	&+&{
	margin-top:3rem;
}
`

const PredictItem=({data})=>{
	const{predict, image}= data;
	return(
		<PredictsItemBlock>
			{image &&(<div className="thumbnail">
					  	<img src={image} alt="thumbnail" />
					  </div>
			)}
			<div className="contents">
				<h2>
					{predict}
				</h2>
			</div>
		</PredictsItemBlock>
	);
};

export default PredictItem;