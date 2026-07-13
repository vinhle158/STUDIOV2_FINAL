import { Request, Response } from 'express';
import { startServer } from '../server';

let appInstance: any = null;

export default async function handler(req: Request, res: Response) {
  if (!appInstance) {
    console.log('[Vercel] Initializing Serverless Express App...');
    const { app } = await startServer();
    appInstance = app;
  }
  return appInstance(req, res);
}
