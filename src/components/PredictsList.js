import styled from 'styled-components';
import PredictsItem from './PredictsItem';
import {useState,useEffect} from 'react';
import axios from 'axios';
import http from "../http-common";
import {MdAdd,MdCheckBoxOutlineBlank,MdCheckBox}  from 'react-icons/md'
import './Insert.scss';

const PredictsListBlock=styled.div`
	box-sizing: border-box;
	padding-bottom: 3rem;
	width:768px;
	margin: 0 auto;
	margin-top:2rem;
	@media screen and (max-widthL 768px){
		width: 100%;
		padding-left:1rem;
		padding-right:1rem;
	}
`;

const sampleArticle={
	predict:'1',
	image:'http'
};


const uploadModule=async (e) =>{
	  const predict=e.target[0].value;
	  const image_file=e.target[1].files[0];
	  
	  const formData=new FormData();
	  formData.append("predict",predict);
	  formData.append("image",image_file);
	  //formData.append("enc")
      http
        .post("/products/",formData,  { headers: {
                "Content-Type": "multipart/form-data",
          },
		})		
        .then(function (response) {
                console.log(response);
        })
        .catch(function (error) {
                console.log(error);
      });  

  }

const PredictsList=({pk})=>{
	
	const [predicts, setPredicts]=useState(null);
	const [loading,setLoading]=useState(false);
	const [liter,setLiter]=useState(false);
	const query = pk === 'all' ? '/products' : `/predict/product/${pk}`
	useEffect(()=>{
		const fetchData=async()=>{
			setLoading(true);
			try{
				const reponse = await axios.get(
					http
						.get(`${query}.json`)
						.then((response) => {
							setPredicts([...response.data]);
							console.log(response.data);
						})
						.catch(function (error) {
							console.log(error);
						})
	  	  			);
			} catch(e){
				console.log(e);
			}
			setLoading(false);
		};
		fetchData();
	}, []);
	
	if (loading){
		return <PredictsListBlock>로딩 중</PredictsListBlock>;
	}
	if (!predicts){
		return null;
	}
	


	
	
return(
		
	<PredictsListBlock>
			
		<form onSubmit={uploadModule} className="Insert">
			name<input type="text" name="predict"/>
				<br />
			image <input type="file" name="image" />
			<button type="submit" value="SUBMIT"><MdAdd/></button>
		</form>	
		
		<br/>
			
		{predicts.map(predict=>(
			<PredictsItem key={predict.predict} data={predict} />
		))}
	</PredictsListBlock>
);
};

export default PredictsList;