CREATE TABLE IF NOT EXISTS lessons (
    id BIGSERIAL PRIMARY KEY,
    subject VARCHAR(120) NOT NULL,
    room VARCHAR(60) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'new',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_status
        CHECK (status IN ('new', 'in_progress', 'done'))
);

INSERT INTO lessons (subject, room, status) VALUES
('Хмарні технології та обчислення', 'ауд. 214', 'in_progress'),
('Бази даних', 'ауд. 105', 'new'),
('Англійська мова', 'ауд. 301', 'done');
