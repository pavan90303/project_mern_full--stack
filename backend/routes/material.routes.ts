import { Router, Request, Response } from 'express';
import { getStore(req), tenantManager } from '../store/storage';\nimport { getStore } from '../middleware/auth';
import { emitToCohort, emitToRole, emitToAll } from '../socket';

const router = Router();

// GET /api/materials
router.get('/', (req: Request, res: Response) => {
  const { subjectId, semester, departmentId, section } = req.query;
  const data = getStore(req).getData();

  let list = data.studyMaterials;
  if (subjectId) {
    list = list.filter(m => m.subjectId === subjectId);
  }
  if (semester) {
    list = list.filter(m => m.semester === Number(semester));
  }
  if (departmentId && departmentId !== 'all') {
    const deptSubjectIds = data.subjects.filter(s => s.departmentId === departmentId).map(s => s.id);
    list = list.filter(m => deptSubjectIds.includes(m.subjectId));
  }
  if (section && section !== 'all' && section !== 'All') {
    list = list.filter(m => !m.section || m.section === 'all' || m.section === 'All' || m.section === section);
  }

  return res.json(list);
});

// POST /api/materials
router.post('/', (req: Request, res: Response) => {
  const { subjectId, title, description, type, url, fileSize, fileName, fileData, semester, section, departmentId } = req.body;
  if (!subjectId || !title) {
    return res.status(400).json({ error: 'Subject and Title are required.' });
  }

  const data = getStore(req).getData();
  const subject = data.subjects.find(s => s.id === subjectId || s.code === subjectId);
  const user = (req as any).user;

  const newMaterial = {
    id: `mat_${Date.now()}`,
    subjectId: subject ? subject.id : subjectId,
    subjectCode: subject ? subject.code : 'CS401',
    subjectName: subject ? subject.name : 'Study Material',
    departmentId: departmentId || (subject ? subject.departmentId : 'dept_cse'),
    facultyId: user?.id || 'usr_fac_01',
    facultyName: user?.name || 'Prof. Marcus Vance',
    title: title.trim(),
    description: description || '',
    type: type || 'pdf',
    fileName: fileName || `${title.replace(/\s+/g, '_')}.pdf`,
    fileSize: fileSize || '2.4 MB',
    fileData: fileData || '',
    url: url || fileData || `#download-${Date.now()}`,
    downloadCount: 0,
    uploadDate: new Date().toISOString().split('T')[0],
    semester: Number(semester) || (subject ? subject.semester : 6),
    section: section || 'All'
  };

  data.studyMaterials.unshift(newMaterial);
  getStore(req).save();

  const deptId = subject ? subject.departmentId : 'dept_cse';
  emitToCohort(deptId, newMaterial.semester, newMaterial.section, 'material:created', newMaterial);
  emitToRole('student', 'material:created', newMaterial);
  emitToRole('faculty', 'material:created', newMaterial);
  emitToAll('material:created', newMaterial);

  getStore(req).logAudit(
    'Study Material Uploaded',
    user?.name || 'Faculty',
    'faculty',
    `Material ${newMaterial.title}`,
    `Added ${newMaterial.type} for ${newMaterial.subjectCode}`
  );

  return res.status(201).json(newMaterial);
});

// DELETE /api/materials/:id
router.delete('/:id', (req: Request, res: Response) => {
  const { id } = req.params;
  const data = getStore(req).getData();
  const material = data.studyMaterials.find(m => m.id === id);
  if (!material) {
    return res.status(404).json({ error: 'Study material not found.' });
  }

  data.studyMaterials = data.studyMaterials.filter(m => m.id !== id);
  getStore(req).save();

  emitToRole('student', 'material:deleted', { id, title: material.title });
  emitToRole('faculty', 'material:deleted', { id, title: material.title });
  emitToAll('material:deleted', { id, title: material.title });

  getStore(req).logAudit(
    'Study Material Removed',
    (req as any).user?.name || 'Faculty',
    'faculty',
    `Material ${material.title}`,
    `Deleted resource`
  );

  return res.json({ message: 'Study material deleted successfully', id });
});

// POST /api/materials/:id/download
router.post('/:id/download', (req: Request, res: Response) => {
  const { id } = req.params;
  const data = getStore(req).getData();
  const material = data.studyMaterials.find(m => m.id === id);
  if (!material) {
    return res.status(404).json({ error: 'Study material not found.' });
  }

  material.downloadCount = (material.downloadCount || 0) + 1;
  getStore(req).save();
  return res.json({ downloadCount: material.downloadCount });
});

export default router;

