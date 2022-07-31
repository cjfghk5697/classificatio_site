import React, { useState } from "react";
import axios from "axios";
import http from "./http-common";





function RestAPI() {
  const [text, setText] = useState([]);

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


          POST
        <button
          onClick={() => {
            http
              .get("/products/")
              .then((response) => {
                setText([...response.data]);
                console.log(response.data);
              })
              .catch(function (error) {
                console.log(error);
              });
          }}
        >
          GET
        </button>
      </div>
	  
	  
	  
      {text.map((e) => (
        <div>
          {" "}
          <div className="list">
            <span>
              {e.predict},
			  <img src={e.image} />
            </span>
            <button
              className="btn-delete"
              onClick={() => {
                http.delete(`/products/${e.id}`);
                setText(text.filter((text) => text.id !== e.id));
              }}
            >
              DELETE
            </button>{" "}
          </div>
        </div>
      ))}
    </>
  );
}

export default RestAPI;