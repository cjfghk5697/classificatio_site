import React, { useState } from "react";
import axios from "axios";

function RestAPI() {
  const [text, setText] = useState([]);

  return (
    <>
      <h1>REST API 연습</h1>
      <div className="btn-primary">
        <button
          onClick={() => {
            axios
              .post("http://127.0.0.1:8000/api/product/",{}, {
                name: "이름",
                price: "가격",
              })
              .then(function (response) {
                console.log(response);
              })
              .catch(function (error) {
                console.log(error);
              });
          }}
        >

          POST
        </button>
        <button
          onClick={() => {
            axios
              .get("http://8000-cjfghk5697-playtorchdis-kit0zg7omnl.ws-us54.gitpod.io/api/product/")
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
              {e.id}번, {e.name}, {e.price}, {e.created_at}
            </span>
            <button
              className="btn-delete"
              onClick={() => {
                axios.delete(`http://127.0.0.1:8000/api/product/${e.id}`);
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