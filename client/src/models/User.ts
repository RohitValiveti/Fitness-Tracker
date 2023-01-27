import { Workout } from "./Exercise";

type SimpleUser = {
  id: number;
  username: string;
};

export type User = {
  id: number;
  username: string;
  password: string;
  sessionToken: string;
  updateToken: string;
  sessionExpiration: string;
  workouts: [Workout];
  friends: [SimpleUser];
  healthFiles: [HealthFile];
};

export type HealthFile = {
  id: number;
  name: string;
  link: string;
  userId: number;
};
