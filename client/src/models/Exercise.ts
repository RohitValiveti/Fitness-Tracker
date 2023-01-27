export type Workout = {
  id: number;
  timeStarted: string;
  timeEnded: string;
  muscleGroup: string;
  exercises: [Exercise];
  userId: number;
};

export type Exercise = {
  id: number;
  exerciseName: string;
  muscle: string;
  sets: [Set];
  workoutId: number;
};

export type Set = {
  Ii: number;
  weight: number;
  reps: number;
  exercisesId: number;
};
