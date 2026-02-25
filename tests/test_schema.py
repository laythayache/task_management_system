import { PrismaClient } from '@prisma/client';
import bcrypt from 'bcrypt';

const prisma = new PrismaClient();

describe('Task Management System Database Schema', () => {
  beforeAll(async () => {
    await prisma.$connect();
  });

  afterAll(async () => {
    await prisma.$disconnect();
  });

  test('createUser_happyPath', async () => {
    const hashedPassword = await bcrypt.hash('user123', 10);
    const user = await prisma.user.create({
      data: {
        username: 'testuser',
        email: 'testuser@example.com',
        passwordHash: hashedPassword,
        role: 'USER',
      },
    });
    expect(user.username).toBe('testuser');
    expect(user.email).toBe('testuser@example.com');
  });

  test('createUser_duplicateUsername', async () => {
    const hashedPassword = await bcrypt.hash('user123', 10);
    await prisma.user.create({
      data: {
        username: 'duplicateUser',
        email: 'dup@example.com',
        passwordHash: hashedPassword,
        role: 'USER',
      },
    });
    await expect(prisma.user.create({
      data: {
        username: 'duplicateUser',
        email: 'another@example.com',
        passwordHash: hashedPassword,
        role: 'USER',
      },
    })).rejects.toThrow();
  });

  test('createDepartment_happyPath', async () => {
    const department = await prisma.department.create({
      data: { name: 'Engineering' },
    });
    expect(department.name).toBe('Engineering');
  });

  test('createTask_happyPath', async () => {
    const user = await prisma.user.findFirst({ where: { username: 'testuser' } });
    const task = await prisma.task.create({
      data: { title: 'Test Task', creatorId: user.id },
    });
    expect(task.title).toBe('Test Task');
  });

  test('createComment_happyPath', async () => {
    const user = await prisma.user.findFirst({ where: { username: 'testuser' } });
    const task = await prisma.task.findFirst({ where: { title: 'Test Task' } });
    const comment = await prisma.comment.create({
      data: { content: 'Nice task!', taskId: task.id, userId: user.id },
    });
    expect(comment.content).toBe('Nice task!');
  });

  test('cascadeDeleteUser', async () => {
    const user = await prisma.user.findFirst({ where: { username: 'testuser' } });
    await prisma.user.delete({ where: { id: user.id } });
    const tasks = await prisma.task.findMany({ where: { creatorId: user.id } });
    expect(tasks.length).toBe(0);
  });

  test('backupDatabase_happyPath', async () => {
    const exec = require('child_process').exec;
    exec('./scripts/db-backup.sh', (err, stdout, stderr) => {
      expect(err).toBeNull();
      expect(stdout).toContain('Backup of your_database_name completed successfully');
    });
  });

  test('restoreDatabase_happyPath', async () => {
    const exec = require('child_process').exec;
    exec('./scripts/db-restore.sh ./backups/db_backup_test.sql', (err, stdout, stderr) => {
      expect(err).toBeNull();
      expect(stdout).toContain('Database restored successfully');
    });
  });
});