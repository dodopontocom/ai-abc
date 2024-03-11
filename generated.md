int _IO_putc(int c, _IO_FILE *f)
{
    while (f->n >= f->p) {
        f->p = f->buf + write(f->fd, f->buf, f->p - f->buf);
        f->n = f->p;
    }
    *f->p = c;
    f->p++;
    return c;
}

