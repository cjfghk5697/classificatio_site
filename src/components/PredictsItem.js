import styled from 'styled-components';
import PercentBar from './Percent'
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

const PredictItem=({data,detail})=>{
	const{predict, image}= data;

	
	
	const url= 'https://disease-onavw.run.goorm.io/'+data.id
	return(
		<PredictsItemBlock className="border-solid border-2 border-indigo-300">
			{detail ==='all' ? 
				(<div className="thumbnail">
					  	<img src={image} alt="thumbnail" />
					  </div>
			) : (<div>
					  	<img className="bg-no-repeat bg-center" src={data.image_url} alt="thumbnail" />
				</div>
			)}
			
			<div className="contents">
				<h2 className="text-semibold hover:font-black">

				{data.answer ?
        		(<p className="text-2xl">
					<a href={url}>Name : {predict} (ID: {data.id})</a> <br/>
					Predict Answer : AI{data.answer}
        		</p>) :
				(
						
						<p className="text-base ">
					<a href={url}>Name : {predict} (ID: {data.id})</a> <br/>
				 	Predict Answer : None
				 </p>
				)
      		}
				</h2>
				<br />

	</div>
					{data.answer && 
				(<div>
					<h1>Percent</h1>
					<PercentBar key={data.id} data={data}/>
				</div>
				)
				}
	</PredictsItemBlock>
	);
};

export default PredictItem;