import {
  Box,
  Button,
  Container,
  Grid,
  SxProps,
  Theme,
  Typography,
} from "@mui/material";
import React from "react";
import FitnessCenterIcon from "@mui/icons-material/FitnessCenter";
import MonitorHeartIcon from "@mui/icons-material/MonitorHeart";
import PeopleIcon from "@mui/icons-material/People";
import { Link as LinkRouter } from "react-router-dom";

const item: SxProps<Theme> = {
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  px: 5,
};

const number = {
  fontSize: 24,
  fontFamily: "default",
  fontWeight: "medium",
  color: "white",
};

const LandingBody = () => {
  return (
    <Box
      component="section"
      sx={{ display: "flex", bgcolor: "primary.main", overflow: "hidden" }}
    >
      <Container
        sx={{
          mt: 10,
          mb: 15,
          position: "relative",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Typography variant="h3" component="h2" sx={{ mb: 14, color: "white" }}>
          How It Works
        </Typography>
        <Grid container spacing={5}>
          <Grid item xs={12} md={4}>
            <Box sx={item}>
              <Box sx={number}>1</Box>
              <Box>
                <FitnessCenterIcon
                  fontSize="large"
                  sx={{ color: "white", padding: 4 }}
                />
              </Box>
              <Typography variant="h5" align="center" sx={{ color: "white" }}>
                Track Fitness Goals.
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={12} md={4}>
            <Box sx={item}>
              <Box sx={number}>2</Box>
              <Box>
                <MonitorHeartIcon
                  fontSize="large"
                  sx={{ color: "white", padding: 4 }}
                />
              </Box>
              <Typography variant="h5" align="center" sx={{ color: "white" }}>
                Track Health Trends.
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={12} md={4}>
            <Box sx={item}>
              <Box sx={number}>3</Box>
              <Box>
                <PeopleIcon
                  fontSize="large"
                  sx={{ color: "white", padding: 4 }}
                />
              </Box>
              <Typography variant="h5" align="center" sx={{ color: "white" }}>
                Find fitness friends.
              </Typography>
            </Box>
          </Grid>
        </Grid>
        <LinkRouter to={`/register`} style={{ textDecoration: "none" }}>
          <Button
            color="info"
            size="large"
            variant="contained"
            component="a"
            sx={{ mt: 8 }}
          >
            Register Now
          </Button>
        </LinkRouter>
      </Container>
    </Box>
  );
};

export default LandingBody;
