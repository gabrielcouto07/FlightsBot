import { create } from 'zustand';
import { User } from '../api/users';

interface UserStore {
  currentUser: User | null;
  users: User[];
  setCurrentUser: (user: User | null) => void;
  setUsers: (users: User[]) => void;
  addUser: (user: User) => void;
  removeUser: (userId: string) => void;
}

export const useUserStore = create<UserStore>((set) => ({
  currentUser: null,
  users: [],

  setCurrentUser: (user: User | null) => set({ currentUser: user }),

  setUsers: (users: User[]) => set({ users }),

  addUser: (user: User) =>
    set((state) => ({
      users: [user, ...state.users],
    })),

  removeUser: (userId: string) =>
    set((state) => ({
      users: state.users.filter((u) => u.id !== userId),
    })),
}));
