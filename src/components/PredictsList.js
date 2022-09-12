import styled from 'styled-components';
import PredictsItem from './PredictsItem';
import {useState,useEffect} from 'react';
import axios from 'axios';
import http from "../http-common";
import './Insert.scss';
import Loader from './Loader';
           
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
		},{
			withCredentials: true // 쿠키 cors 통신 설정
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
	const query = pk === 'all' ? '/products' : `/predict/product/${pk}`
	useEffect(()=>{
		const fetchData=async()=>{
			setLoading(true);
			try{
				const reponse = await axios.get(
					http
						.get(`${query}`)
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
		return (<Loader type="spin" color="#00BFFF" message="Loading.."/>);
	}
	if (!predicts){
		return null;
	}
	


	
	
return(
		
	<PredictsListBlock>
			
		<form onSubmit={uploadModule} className="rounded-md border-4">
			<p className="pl-2 pt-1 font-semibold text-xl hover:font-black">Title</p><input type="text" name="predict" placeholder="이름" className="placeholder:italic placeholder:text-slate-400 block bg-white w-full border border-slate-300 rounded-md py-2 pl-9 pr-3 shadow-sm focus:outline-none focus:border-sky-500 focus:ring-sky-500 focus:ring-1 sm:text-sm"/>
			<p className="pl-2 font-semibold text-xl hover:font-black">Image</p> <input type="file" name="image" className="block w-full text-sm text-slate-500
      file:mr-4 file:py-2 file:px-4
      file:rounded-full file:border-0
      file:text-sm file:font-semibold
      file:bg-violet-50 file:text-violet-700
      hover:file:bg-violet-100"/> 
			<button type="submit" value="SUBMIT" className="w-40 h-8 my-3 mx-2 text-white text-xl font-semibold align-middle rounded-full bg-sky-500 hover:bg-sky-700">Save</button>
		</form>
		
		<br/>
			
		{predicts.map(predict=>(
			<PredictsItem key={predict.id} data={predict} detail={pk} />
		))}
	</PredictsListBlock>
);
};

export default PredictsList;