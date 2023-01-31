import React, { useState } from "react";
import { useParams } from "react-router-dom";
import { Workout } from "../models/Exercise";
import axios from "axios";

const Home = () => {
  const { userId } = useParams();
  const [workout, setWorkout] = useState<Workout>();
  function getData() {
    axios({
      method: "GET",
      url: "/workouts/"+userId,
    })
      .then((response) => {
        const res = response.data;
        console.log(res)
        setWorkout({
          id: res.id,
          timeStarted: res.time_started,
          timeEnded: res.time_ended,
          muscleGroup: res.muscle_group,
          exercises: res.exercises,
          userId: res.user_id,
        });
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
          console.log(error.response.status);
          console.log(error.response.headers);
        }
      });
  }

  return (
    <>
      <h3>Home Page</h3>
      UserId: {userId}
      <br></br>
      <button onClick={getData}>click me</button>
      <br></br>
      workout_id: {workout ? workout.id : "None"}
      <br></br>
      time started: {workout ? workout.timeStarted : "None"}
      <br></br>
      time started: {workout ? workout.timeEnded : "None"}
      <br></br>
      muscle group: {workout ? workout.muscleGroup : "None"}
      <br></br>
      {/* exercises: {workout ? workout.exercises : "None"} */}
      <br></br>
      {/* user id: {workout ? workout.userId : "None"} */}
      

    </>
  );
};

export default Home;
