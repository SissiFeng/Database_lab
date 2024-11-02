-- 启用UUID扩展（如果使用PostgreSQL）
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 创建实验状态的枚举类型
CREATE TYPE experiment_status AS ENUM (
    'planned',    -- 已计划
    'setup',      -- 准备中
    'running',    -- 进行中
    'paused',     -- 已暂停
    'completed',  -- 已完成
    'failed',     -- 失败
    'cancelled'   -- 已取消
);

-- 创建实验表
CREATE TABLE IF NOT EXISTS experiments (
    -- 基本标识
    experiment_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    experiment_code VARCHAR(50) UNIQUE NOT NULL,  -- 实验编号，方便人工引用
    
    -- 基本信息
    name VARCHAR(255) NOT NULL,
    description TEXT,
    
    -- 实验配置
    protocol_version VARCHAR(50) NOT NULL,        -- 实验协议版本
    target_temperature DECIMAL(5,2),              -- 目标温度
    target_pressure DECIMAL(8,2),                 -- 目标压力
    target_duration INTERVAL,                     -- 预期持续时间
    
    -- 时间追踪
    planned_start_time TIMESTAMP WITH TIME ZONE,  -- 计划开始时间
    actual_start_time TIMESTAMP WITH TIME ZONE,   -- 实际开始时间
    actual_end_time TIMESTAMP WITH TIME ZONE,     -- 实际结束时间
    
    -- 状态管理
    status experiment_status NOT NULL DEFAULT 'planned',
    status_changed_at TIMESTAMP WITH TIME ZONE,   -- 状态最后更改时间
    
    -- 实验配置和结果
    configuration JSONB NOT NULL DEFAULT '{}',    -- 详细配置参数
    results_summary JSONB,                        -- 实验结果摘要
    
    -- 审计字段
    created_by VARCHAR(100) NOT NULL,            -- 创建者
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100),                     -- 最后更新者
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- 约束条件
    CONSTRAINT valid_dates CHECK (
        actual_start_time <= actual_end_time
    ),
    CONSTRAINT valid_temperature CHECK (
        target_temperature BETWEEN -273.15 AND 1000
    ),
    CONSTRAINT valid_pressure CHECK (
        target_pressure >= 0
    )
);

-- 创建触发器函数：自动更新 updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 创建触发器：更新 updated_at
CREATE TRIGGER update_experiments_updated_at
    BEFORE UPDATE ON experiments
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 创建触发器函数：记录状态变更时间
CREATE OR REPLACE FUNCTION update_status_changed_at()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.status IS NULL OR NEW.status != OLD.status THEN
        NEW.status_changed_at = CURRENT_TIMESTAMP;
    END IF;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 创建触发器：更新状态变更时间
CREATE TRIGGER update_experiments_status_changed_at
    BEFORE UPDATE ON experiments
    FOR EACH ROW
    EXECUTE FUNCTION update_status_changed_at();

-- 创建样品类型枚举
CREATE TYPE sample_type AS ENUM (
    'raw_material',      -- 原材料
    'intermediate',      -- 中间产物
    'final_product',     -- 最终产品
    'control',           -- 对照样品
    'standard'           -- 标准样品
);

-- 创建样品状态枚举
CREATE TYPE sample_status AS ENUM (
    'prepared',          -- 已制备
    'in_analysis',       -- 分析中
    'completed',         -- 已完成
    'disposed',          -- 已处置
    'stored'            -- 已存储
);

-- 创建样品表
CREATE TABLE IF NOT EXISTS samples (
    -- 基本标识
    sample_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sample_code VARCHAR(50) UNIQUE NOT NULL,      -- 样品编号
    experiment_id UUID NOT NULL REFERENCES experiments(experiment_id),
    
    -- 基本信息
    name VARCHAR(255) NOT NULL,
    type sample_type NOT NULL,
    status sample_status NOT NULL DEFAULT 'prepared',
    
    -- 样品特性
    material_type VARCHAR(100) NOT NULL,          -- 材料类型
    mass DECIMAL(10,4),                           -- 质量(g)
    volume DECIMAL(10,4),                         -- 体积(ml)
    concentration DECIMAL(10,4),                  -- 浓度(mol/L)
    
    -- 制备信息
    preparation_date TIMESTAMP WITH TIME ZONE NOT NULL,
    preparation_method TEXT,                      -- 制备方法
    preparation_conditions JSONB NOT NULL DEFAULT '{}',  -- 制备条件
    
    -- 存储信息
    storage_location VARCHAR(100),                -- 存储位置
    storage_conditions JSONB,                     -- 存储条件
    expiration_date TIMESTAMP WITH TIME ZONE,     -- 有效期
    
    -- 质量控制
    quality_status VARCHAR(50),                   -- 质量状态
    quality_notes TEXT,                           -- 质量备注
    
    -- 父子样品关系（用于追踪样品派生关系）
    parent_sample_id UUID REFERENCES samples(sample_id),
    
    -- 审计字段
    created_by VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- 约束条件
    CONSTRAINT valid_mass CHECK (mass > 0),
    CONSTRAINT valid_volume CHECK (volume > 0),
    CONSTRAINT valid_concentration CHECK (concentration >= 0),
    CONSTRAINT valid_dates CHECK (
        preparation_date <= CURRENT_TIMESTAMP AND
        (expiration_date IS NULL OR expiration_date > preparation_date)
    )
);

-- 创建触发器：更新 updated_at
CREATE TRIGGER update_samples_updated_at
    BEFORE UPDATE ON samples
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 创建样品历史表（用于追踪样品状态变更）
CREATE TABLE IF NOT EXISTS sample_history (
    history_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sample_id UUID NOT NULL REFERENCES samples(sample_id),
    changed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    changed_by VARCHAR(100) NOT NULL,
    old_status sample_status,
    new_status sample_status NOT NULL,
    change_reason TEXT,
    notes TEXT
);

-- 创建触发器函数：记录样品状态变更
CREATE OR REPLACE FUNCTION log_sample_status_change()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.status IS NULL OR NEW.status != OLD.status THEN
        INSERT INTO sample_history (
            sample_id,
            changed_by,
            old_status,
            new_status,
            change_reason
        ) VALUES (
            NEW.sample_id,
            NEW.updated_by,
            OLD.status,
            NEW.status,
            'Status changed by system'
        );
    END IF;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 创建触发器：样品状态变更日志
CREATE TRIGGER log_sample_status_changes
    AFTER UPDATE OF status ON samples
    FOR EACH ROW
    EXECUTE FUNCTION log_sample_status_change();

-- 创建图像类型枚举
CREATE TYPE image_type AS ENUM (
    'microscope',        -- 显微镜图像
    'spectroscopy',      -- 光谱图像
    'thermal',           -- 热成像
    'time_lapse',        -- 延时摄影
    'raw_data'          -- 原始数据
);

-- 创建图像质量枚举
CREATE TYPE image_quality AS ENUM (
    'excellent',
    'good',
    'fair',
    'poor',
    'unusable'
);

-- 创建图像表
CREATE TABLE IF NOT EXISTS images (
    -- 基本标识
    image_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    image_code VARCHAR(50) UNIQUE NOT NULL,
    
    -- 关联关系
    experiment_id UUID NOT NULL REFERENCES experiments(experiment_id),
    sample_id UUID NOT NULL REFERENCES samples(sample_id),
    
    -- 图像信息
    image_type image_type NOT NULL,
    file_path TEXT NOT NULL,                      -- S3或存储路径
    file_name VARCHAR(255) NOT NULL,
    file_format VARCHAR(10) NOT NULL,             -- 如 'TIFF', 'JPG'
    file_size BIGINT NOT NULL,                    -- 字节数
    
    -- 采集参数
    capture_time TIMESTAMP WITH TIME ZONE NOT NULL,
    device_id VARCHAR(100) NOT NULL,              -- 设备ID
    device_settings JSONB NOT NULL DEFAULT '{}',   -- 设备参数
    
    -- 图像属性
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    resolution VARCHAR(50),                        -- 如 '300dpi'
    bit_depth INTEGER,                            -- 位深度
    channels INTEGER,                             -- 通道数
    
    -- 质量控制
    quality_score image_quality NOT NULL,
    quality_notes TEXT,
    is_valid BOOLEAN DEFAULT true,
    
    -- 元数据
    metadata JSONB NOT NULL DEFAULT '{}',          -- 其他元数据
    tags TEXT[],                                   -- 标签数组
    
    -- 审计字段
    created_by VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- 约束条件
    CONSTRAINT valid_dimensions CHECK (width > 0 AND height > 0),
    CONSTRAINT valid_file_size CHECK (file_size > 0)
);

-- 创建分析结果表
CREATE TABLE IF NOT EXISTS analysis_results (
    -- 基本标识
    result_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    result_code VARCHAR(50) UNIQUE NOT NULL,
    
    -- 关联关系
    experiment_id UUID NOT NULL REFERENCES experiments(experiment_id),
    sample_id UUID NOT NULL REFERENCES samples(sample_id),
    image_id UUID REFERENCES images(image_id),    -- 可选，不是所有分析都基于图像
    
    -- 分析信息
    analysis_type VARCHAR(100) NOT NULL,          -- 分析类型
    analysis_version VARCHAR(50) NOT NULL,        -- 分析软件/方法版本
    analysis_parameters JSONB NOT NULL DEFAULT '{}', -- 分析参数
    
    -- 结果数据
    result_data JSONB NOT NULL,                   -- 分析结果
    result_summary TEXT,                          -- 结果摘要
    confidence_score DECIMAL(5,4),                -- 置信度分数
    
    -- 质量控制
    validation_status VARCHAR(50),                -- 验证状态
    validation_notes TEXT,                        -- 验证备注
    is_valid BOOLEAN DEFAULT true,
    
    -- 时间信息
    started_at TIMESTAMP WITH TIME ZONE NOT NULL,
    completed_at TIMESTAMP WITH TIME ZONE NOT NULL,
    processing_duration INTERVAL,                 -- 处理时长
    
    -- 审计字段
    created_by VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- 约束条件
    CONSTRAINT valid_confidence CHECK (
        confidence_score IS NULL OR 
        (confidence_score >= 0 AND confidence_score <= 1)
    ),
    CONSTRAINT valid_analysis_times CHECK (
        started_at <= completed_at
    )
);

-- 为所有表创建更新触发器
CREATE TRIGGER update_images_updated_at
    BEFORE UPDATE ON images
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_analysis_results_updated_at
    BEFORE UPDATE ON analysis_results
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 创建常用索引
CREATE INDEX idx_images_experiment_sample ON images(experiment_id, sample_id);
CREATE INDEX idx_images_capture_time ON images(capture_time);
CREATE INDEX idx_images_type ON images(image_type);
CREATE INDEX idx_analysis_experiment_sample ON analysis_results(experiment_id, sample_id);
CREATE INDEX idx_analysis_type ON analysis_results(analysis_type);
CREATE INDEX idx_analysis_validation ON analysis_results(validation_status);

