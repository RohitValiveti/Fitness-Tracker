export type Workout = {
  id: number;
  timeStarted: string;
  timeEnded: string;
  muscleGroup: string;
  exercises: [SimpleExercise];
  userId: number;
};

type SimpleExercise = {
  id: number;
  exerciseName: string;
  muscle: string;
  workoutId: number;
};

export type Exercise = {
  id: number;
  exerciseName: string;
  muscle: string;
  sets: [Set];
  workoutId: number;
};

export type Set = {
  id: number;
  weight: number;
  reps: number;
  exercisesId: number;
};
