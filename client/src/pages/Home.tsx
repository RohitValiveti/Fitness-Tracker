import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { LoginUser } from "../models/User";
import axios from "axios";

const Home = () => {
  const { userId } = useParams();
  const [user, setUser] = useState<LoginUser>();
  const session_token = "9c8afacf221c1ddaecf5b925d564f80b78d6df5f";
  const headers = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${session_token}`,
  };
  

  useEffect(() => {
    axios.get("/users/" + userId, )
    axios({
      method: "GET",
      url: "/users/" + userId,
      headers: headers,
    })
      .then((response) => {
        const res = response.data;
        console.log(res);
        setUser({
          id: res.id,
          email: res.email,
          workouts: res.workouts,
          friends: res.friends,
        });
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
          console.log(error.response.status);
          console.log(error.response.headers);
        }
      });
  }, []);

  return (
    <>
      <h3>Home Page</h3>
      <br></br>
      email: {user ? user.email : "None"}
      <br></br>
      {/* Workouts: {user ? user.workouts : "None"}
      <br></br>
      Friends: {user ? user.friends : "None"}
      <br></br> */}
    </>
  );
};

export default Home;
