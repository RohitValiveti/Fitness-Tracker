import React from "react";

const Footer = () => {
  return (
    <div
      style={{
        textAlign: "center",
        padding: 28,
      }}
    >
      © {new Date().getFullYear()} Copyright:
      <a
        href="https://rohitvaliveti.github.io"
        target="_blank"
        rel="noreferrer"
      >
        Rohit Valiveti
      </a>
    </div>
  );
};

export default Footer;
