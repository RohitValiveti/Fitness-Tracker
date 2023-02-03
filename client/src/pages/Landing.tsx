import React from "react";
import AppAppBar from "../components/AppBar";
import Footer from "../components/Footer";
import LandingBody from "../components/LandingBody";

const Landing = () => {
  return (
    <React.Fragment>
      <AppAppBar />
      <LandingBody />
      <Footer />
    </React.Fragment>
  );
};

export default Landing;
