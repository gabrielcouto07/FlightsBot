import { User } from '../../api/users';
import { Badge, Button } from '../ui';
import { Trash2, Edit2 } from 'lucide-react';

interface UserRowProps {
  user: User;
  onEdit?: (user: User) => void;
  onDelete?: (userId: string) => void;
}

export const UserRow = ({ user, onEdit, onDelete }: UserRowProps) => {
  return (
    <div className="bg-bg-secondary border border-border-primary rounded-lg p-4 flex items-center justify-between hover:bg-bg-tertiary transition-colors">
      <div className="flex-1">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-teal rounded-full flex items-center justify-center text-bg-primary font-bold">
            {user.name?.[0]?.toUpperCase() || '?'}
          </div>
          <div>
            <p className="font-semibold text-primary">{user.name || 'Unnamed User'}</p>
            <p className="text-sm text-tertiary">{user.phone_number}</p>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-3">
        <Badge variant={user.plan === 'paid' ? 'teal' : 'info'}>
          {user.plan === 'paid' ? 'Premium' : 'Free'}
        </Badge>
        <Badge variant={user.is_active ? 'success' : 'danger'}>
          {user.is_active ? 'Active' : 'Inactive'}
        </Badge>

        <div className="flex gap-2">
          {onEdit && (
            <Button
              size="sm"
              variant="secondary"
              onClick={() => onEdit(user)}
              className="p-2"
            >
              <Edit2 size={16} />
            </Button>
          )}
          {onDelete && (
            <Button
              size="sm"
              variant="danger"
              onClick={() => onDelete(user.id)}
              className="p-2"
            >
              <Trash2 size={16} />
            </Button>
          )}
        </div>
      </div>
    </div>
  );
};
