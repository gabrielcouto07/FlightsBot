import { useState, useEffect } from 'react';
import { Layout } from '../components/layout/Layout';
import { Card, Button, EmptyState } from '../components/ui';
import { usersAPI, User } from '../api/users';
import { UserRow } from '../components/users/UserRow';
import { UserModal } from '../components/users/UserModal';
import { Plus } from 'lucide-react';

export const UsersManager = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    setIsLoading(true);
    try {
      const data = await usersAPI.listUsers();
      setUsers(data);
    } catch (error) {
      console.error('Load error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSave = async (data: { phone_number: string; name?: string; plan: 'free' | 'paid' }) => {
    try {
      if (selectedUser) {
        await usersAPI.updateUser(selectedUser.id, data);
      } else {
        await usersAPI.createUser(data);
      }
      setIsModalOpen(false);
      setSelectedUser(null);
      await loadUsers();
    } catch (error) {
      console.error('Save error:', error);
    }
  };

  const handleDelete = async (userId: string) => {
    if (confirm('Are you sure?')) {
      try {
        await usersAPI.deleteUser(userId);
        await loadUsers();
      } catch (error) {
        console.error('Delete error:', error);
      }
    }
  };

  return (
    <Layout>
      <div className="p-6 max-w-4xl mx-auto space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">Users Manager</h1>
            <p className="text-tertiary mt-1">Manage demo users and their plans</p>
          </div>
          <Button
            variant="primary"
            onClick={() => {
              setSelectedUser(null);
              setIsModalOpen(true);
            }}
          >
            <Plus size={18} />
            New User
          </Button>
        </div>

        <Card>
          {isLoading ? (
            <div className="text-center py-8">Loading...</div>
          ) : users.length === 0 ? (
            <EmptyState
              icon="👥"
              title="No users yet"
              description="Create your first demo user"
              action={
                <Button
                  variant="primary"
                  onClick={() => {
                    setSelectedUser(null);
                    setIsModalOpen(true);
                  }}
                >
                  Create User
                </Button>
              }
            />
          ) : (
            <div className="space-y-2">
              {users.map((user) => (
                <UserRow
                  key={user.id}
                  user={user}
                  onEdit={() => {
                    setSelectedUser(user);
                    setIsModalOpen(true);
                  }}
                  onDelete={handleDelete}
                />
              ))}
            </div>
          )}
        </Card>

        <UserModal
          isOpen={isModalOpen}
          onClose={() => {
            setIsModalOpen(false);
            setSelectedUser(null);
          }}
          user={selectedUser || undefined}
          onSave={handleSave}
        />
      </div>
    </Layout>
  );
};
