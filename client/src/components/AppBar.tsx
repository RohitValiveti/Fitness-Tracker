import MuiAppBar, { AppBarProps } from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Link from "@mui/material/Link";
import { styled } from "@mui/material/styles";
import MuiToolbar from "@mui/material/Toolbar";
import { Link as LinkRouter } from "react-router-dom";

const Toolbar = styled(MuiToolbar)(({ theme }) => ({
  height: 64,
  [theme.breakpoints.up("sm")]: {
    height: 70,
  },
}));

function AppBar(props: AppBarProps) {
  return <MuiAppBar elevation={0} position="fixed" {...props} />;
}

const rightLink = {
  fontSize: 16,
  color: "common.white",
  ml: 3,
};

const AppAppBar = () => {
  return (
    <div>
      <AppBar position="fixed">
        <Toolbar sx={{ justifyContent: "space-between" }}>
          <Box
            sx={{
              flex: 1,
              mt: 10,
              mb: 15,
              position: "relative",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
            }}
          />
          <Link
            variant="h6"
            underline="none"
            color="inherit"
            href="https://rohitvaliveti.github.io"
            sx={{ fontSize: 24 }}
            target="_blank"
          >
            {"Fitness Tracker"}
          </Link>
          <Box sx={{ flex: 1, display: "flex", justifyContent: "flex-end" }}>
            <LinkRouter to={`/register`} style={{ textDecoration: "none" }}>
              <Link
                color="inherit"
                variant="h6"
                underline="none"
                sx={rightLink}
              >
                {"Sign Up"}
              </Link>
            </LinkRouter>

            <LinkRouter to={`/login`} style={{ textDecoration: "none" }}>
              <Link
                color="inherit"
                variant="h6"
                underline="none"
                sx={rightLink}
              >
                {"Sign In"}
              </Link>
            </LinkRouter>
          </Box>
        </Toolbar>
      </AppBar>
      <Toolbar />
    </div>
  );
};

export default AppAppBar;
