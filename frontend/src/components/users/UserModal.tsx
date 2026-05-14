import { useEffect, useState } from 'react';
import { User } from '../../api/users';
import { Modal, Input, Select, Button } from '../ui';

interface UserModalProps {
  isOpen: boolean;
  onClose: () => void;
  user?: User;
  onSave: (data: { phone_number: string; name?: string; plan: 'free' | 'paid' }) => void;
  isLoading?: boolean;
}

export const UserModal = ({
  isOpen,
  onClose,
  user,
  onSave,
  isLoading = false,
}: UserModalProps) => {
  const [formData, setFormData] = useState({
    phone_number: user?.phone_number || '',
    name: user?.name || '',
    plan: user?.plan || 'free' as 'free' | 'paid',
  });

  useEffect(() => {
    setFormData({
      phone_number: user?.phone_number || '',
      name: user?.name || '',
      plan: user?.plan || 'free',
    });
  }, [user, isOpen]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSave(formData);
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={user ? 'Edit User' : 'New User'}>
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          label="Phone Number"
          type="tel"
          placeholder="55XXXXXXXXXXXXX"
          value={formData.phone_number}
          onChange={(e) => setFormData({ ...formData, phone_number: e.target.value })}
          required
        />

        <Input
          label="Name"
          type="text"
          placeholder="User name"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
        />

        <Select
          label="Plan"
          options={[
            { value: 'free', label: 'Free' },
            { value: 'paid', label: 'Paid' },
          ]}
          value={formData.plan}
          onChange={(e) => setFormData({ ...formData, plan: e.target.value as 'free' | 'paid' })}
        />

        <div className="flex gap-2 pt-4">
          <Button type="button" variant="secondary" onClick={onClose} className="flex-1">
            Cancel
          </Button>
          <Button type="submit" variant="primary" isLoading={isLoading} className="flex-1">
            {user ? 'Update' : 'Create'} User
          </Button>
        </div>
      </form>
    </Modal>
  );
};
