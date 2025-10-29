import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from './ui/table';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Eye } from 'lucide-react';

interface Representante {
  id: string;
  nome: string;
  status: 'Ativo' | 'Inativo';
}

interface RepresentantesTableProps {
  representantes: Representante[];
  onViewRepresentacoes: (id: string) => void;
}

export function RepresentantesTable({ representantes, onViewRepresentacoes }: RepresentantesTableProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Ativo':
        return 'bg-[#dcfce7] text-[#166534] border-[#86efac]';
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
              <TableHead className="font-semibold text-[#003366] py-4 px-4 md:px-6 min-w-[200px]">
                Representantes
              </TableHead>
              <TableHead className="font-semibold text-[#003366] py-4 px-4 md:px-6 w-[180px]">
                Status
              </TableHead>
              <TableHead className="w-[320px]"></TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {representantes.map((representante) => (
              <TableRow 
                key={representante.id}
                className="hover:bg-[#f9fafb] transition-colors"
              >
                <TableCell className="py-4 px-4 md:px-6">
                  <span className="text-[#1a1a1a]">{representante.nome}</span>
                </TableCell>
                <TableCell className="py-4 px-4 md:px-6">
                  <Badge 
                    variant="outline" 
                    className={`${getStatusColor(representante.status)} border font-normal px-3 py-1 whitespace-nowrap`}
                  >
                    {representante.status}
                  </Badge>
                </TableCell>
                <TableCell className="py-4 px-4 md:px-6">
                  <div className="flex items-center gap-2 justify-end">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => onViewRepresentacoes(representante.id)}
                      className="border-[#d1d5db] text-[#1a1a1a] hover:bg-[#f3f4f6] hover:text-[#003366] whitespace-nowrap"
                    >
                      <Eye size={14} className="mr-2" />
                      Visualizar Representações
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
