import React, { useState } from "react";
import http from "./http-common";





function RestAPI() {

  const uploadModule=async (e) =>{
	  e.preventDefault();
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
  const [text, setText] = useState({});

  const usePkNumber=async (e)=>{
	e.preventDefault();
	const number=e.target[0].value;

    http
    	.get(`/predict/product/${number}`)
        .then((response) => {
            setText([...response.data]);
            console.log(response.data);
        })
        .catch(function (error) {
        	console.log(error);
    	});
	 
	  	  
    }
  
  
  
  return (
    <>
      <h1>REST API 연습</h1>
      <div>
		<form onSubmit={uploadModule}>
			name<input type="text" name="predict"/>
			<br />
			image <input type="file" name="files" />
			<input type="submit" value="SUBMIT"/>
		</form>	
		 <br />
		POST

		<form onSubmit={usePkNumber}>
		number<input type="text" name="number"/>		  
		<input type="submit" value="SUBMIT"/>
		</form>

    	</div>
	  
	  
          <div className="list">
            <span>
              {text.predict}, {text.answer}
			  <img src={text.image} />
            </span>

          </div>
    </>
  );
}

export default RestAPI;