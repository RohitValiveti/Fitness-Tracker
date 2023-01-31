import App from "./App";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import ErrorPage from "./pages/ErrorPage";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Home from "./pages/Home";
// https://reactrouter.com/en/main/start/tutorial -- Helpful page for routing

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/login",
    element: <Login />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/register",
    element: <Register />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/home/:userId",
    element: <Home />,
    errorElement: <ErrorPage />,
  },
]);

const Router = () => <RouterProvider router={router} />;

export default Router;
