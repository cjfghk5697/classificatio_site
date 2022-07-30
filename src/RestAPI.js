import React, { useState } from "react";
import axios from "axios";
import http from "./http-common";

function RestAPI() {
  const [text, setText] = useState([]);

  return (
    <>
      <h1>REST API 연습</h1>
      <div className="btn-primary">
        <button
          onClick={() => {
            http
              .post("/product/", {
                name: "이름",
                price: "가격",
              })
              .then(function (response) {
                console.log(response.json());
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
            http
              .get("/product/")
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
              {e.id}번, {e.name}, {e.price}
            </span>
            <button
              className="btn-delete"
              onClick={() => {
                http.delete(`/${e.id}`);
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