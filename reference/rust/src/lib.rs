//! Illustrative model for Qube CLI Lifecycle Contract v2.
//!
//! This crate is deliberately not a shared product dependency. The normative
//! requirements live under `spec/` at the repository root.

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum OwnershipState {
    Absent,
    Owned,
    Degraded,
    Conflict,
    Unmanaged,
    Unknown,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum LifecycleStatus {
    Succeeded,
    NoChange,
    Cancelled,
    ConfirmationRequired,
    Failed,
    RolledBack,
    RequiresUserAction,
    PendingRestart,
    PendingHandoff,
    RollbackFailed,
}

impl LifecycleStatus {
    #[must_use]
    pub const fn exit_code(self) -> i32 {
        match self {
            Self::Succeeded | Self::NoChange => 0,
            Self::Cancelled | Self::ConfirmationRequired => 1,
            Self::Failed | Self::RolledBack => 2,
            Self::RequiresUserAction | Self::PendingRestart | Self::PendingHandoff => 3,
            Self::RollbackFailed => 4,
        }
    }

    #[must_use]
    pub const fn is_success(self) -> bool {
        self.exit_code() == 0
    }

    #[must_use]
    pub const fn is_final(self) -> bool {
        !matches!(
            self,
            Self::RequiresUserAction | Self::PendingRestart | Self::PendingHandoff
        )
    }
}

/// Abstract discovery inputs. Product adapters replace these booleans with
/// exact package, receipt, payload, and command-resolution evidence.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub struct OwnershipEvidence {
    pub recognized_owner_count: usize,
    pub has_competing_evidence: bool,
    pub has_unknown_target: bool,
    pub has_unmanaged_command: bool,
    pub single_owner_degraded: bool,
}

/// Demonstrates the contract's mutually exclusive classification priority.
#[must_use]
pub const fn classify_ownership(evidence: OwnershipEvidence) -> OwnershipState {
    if evidence.recognized_owner_count > 1
        || (evidence.recognized_owner_count == 1 && evidence.has_competing_evidence)
    {
        OwnershipState::Conflict
    } else if evidence.recognized_owner_count == 0 && evidence.has_unknown_target {
        OwnershipState::Unknown
    } else if evidence.recognized_owner_count == 0 && evidence.has_unmanaged_command {
        OwnershipState::Unmanaged
    } else if evidence.recognized_owner_count == 1 && evidence.single_owner_degraded {
        OwnershipState::Degraded
    } else if evidence.recognized_owner_count == 1 {
        OwnershipState::Owned
    } else {
        OwnershipState::Absent
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn status_exit_mapping_is_closed() {
        let cases = [
            (LifecycleStatus::Succeeded, 0, true),
            (LifecycleStatus::NoChange, 0, true),
            (LifecycleStatus::Cancelled, 1, false),
            (LifecycleStatus::ConfirmationRequired, 1, false),
            (LifecycleStatus::Failed, 2, false),
            (LifecycleStatus::RolledBack, 2, false),
            (LifecycleStatus::RequiresUserAction, 3, false),
            (LifecycleStatus::PendingRestart, 3, false),
            (LifecycleStatus::PendingHandoff, 3, false),
            (LifecycleStatus::RollbackFailed, 4, false),
        ];
        for (status, exit_code, success) in cases {
            assert_eq!(status.exit_code(), exit_code);
            assert_eq!(status.is_success(), success);
        }
    }

    #[test]
    fn helper_spawn_is_pending_not_success() {
        let status = LifecycleStatus::PendingHandoff;
        assert_eq!(status.exit_code(), 3);
        assert!(!status.is_success());
        assert!(!status.is_final());
    }

    #[test]
    fn conflict_outranks_degraded_owner() {
        let state = classify_ownership(OwnershipEvidence {
            recognized_owner_count: 1,
            has_competing_evidence: true,
            single_owner_degraded: true,
            ..OwnershipEvidence::default()
        });
        assert_eq!(state, OwnershipState::Conflict);
    }

    #[test]
    fn unknown_and_unmanaged_are_not_absence() {
        assert_eq!(
            classify_ownership(OwnershipEvidence {
                has_unknown_target: true,
                ..OwnershipEvidence::default()
            }),
            OwnershipState::Unknown
        );
        assert_eq!(
            classify_ownership(OwnershipEvidence {
                has_unmanaged_command: true,
                ..OwnershipEvidence::default()
            }),
            OwnershipState::Unmanaged
        );
    }
}
