import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from './ui/table';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Edit, Users, Heart } from 'lucide-react';

interface Colegiado {
  id: string;
  nome: string;
  status: 'Ativo' | 'Inativo' | 'Em estruturação';
  numeroRepresentantes: number;
  destacado?: boolean;
}

interface ColegiadosTableProps {
  colegiados: Colegiado[];
  onEdit: (id: string) => void;
  onViewRepresentantes: (id: string) => void;
}

export function ColegiadosTable({ colegiados, onEdit, onViewRepresentantes }: ColegiadosTableProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Ativo':
        return 'bg-[#dcfce7] text-[#166534] border-[#86efac]';
      case 'Em estruturação':
        return 'bg-[#fef3c7] text-[#92400e] border-[#fcd34d]';
      case 'Inativo':
        return 'bg-[#fee2e2] text-[#991b1b] border-[#fca5a5]';
      default:
        return 'bg-[#e5e7eb] text-[#1a1a1a] border-[#d1d5db]';
    }
  };

  return (
    <div className="bg-white rounded-lg border border-border overflow-hidden">
      <div className="overflow-x-auto">
        <Table>
          <TableHeader>
            <TableRow className="bg-[#f9fafb] hover:bg-[#f9fafb]">
              <TableHead className="font-semibold text-[#003366] py-4 px-4 md:px-6 min-w-[250px]">
                Colegiado
              </TableHead>
              <TableHead className="font-semibold text-[#003366] py-4 px-4 md:px-6 w-[180px]">
                Status
              </TableHead>
              <TableHead className="font-semibold text-[#003366] py-4 px-4 md:px-6 text-right w-[200px]">
                Número de Representantes
              </TableHead>
              <TableHead className="w-[300px]"></TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {colegiados.map((colegiado) => (
              <TableRow 
                key={colegiado.id}
                className="hover:bg-[#f9fafb] transition-colors"
              >
                <TableCell className="py-4 px-4 md:px-6">
                  <div className="flex items-center gap-2">
                    <span className="text-[#1a1a1a]">{colegiado.nome}</span>
                    {colegiado.destacado && (
                      <Heart size={16} className="text-[#dc2626] fill-[#dc2626] flex-shrink-0" />
                    )}
                  </div>
                </TableCell>
                <TableCell className="py-4 px-4 md:px-6">
                  <Badge 
                    variant="outline" 
                    className={`${getStatusColor(colegiado.status)} border font-normal px-3 py-1 whitespace-nowrap`}
                  >
                    {colegiado.status}
                  </Badge>
                </TableCell>
                <TableCell className="py-4 px-4 md:px-6 text-right text-[#1a1a1a]">
                  {colegiado.numeroRepresentantes}
                </TableCell>
                <TableCell className="py-4 px-4 md:px-6">
                  <div className="flex items-center gap-2 justify-end">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => onEdit(colegiado.id)}
                      className="border-[#d1d5db] text-[#1a1a1a] hover:bg-[#f3f4f6] hover:text-[#003366] whitespace-nowrap"
                    >
                      <Edit size={14} className="mr-2" />
                      Editar
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => onViewRepresentantes(colegiado.id)}
                      className="border-[#d1d5db] text-[#1a1a1a] hover:bg-[#f3f4f6] hover:text-[#003366] whitespace-nowrap"
                    >
                      <Users size={14} className="mr-2" />
                      Visualizar Representantes
                    </Button>
                  </div>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
