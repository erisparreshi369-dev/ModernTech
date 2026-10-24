using System.Collections.Generic;

// Optional companion to the ModernTech data mod: once your company has released its own AI
// (an AI Assistant, Coding Assistant or Image Generator, in-house or for sale), your employees
// use it and design and develop software twice as fast.
//
// Employee effectiveness is recalculated by the game after every work step, so the boost goes
// into the game's own speed multipliers instead: the difficulty's design and development speed.
// The boosted difficulty is a renamed copy ("Medium +AI"), so a saved game remembers that it
// is already boosted and loading it never doubles the speed twice.
public class ModernTechAI : ModBehaviour
{
	public const float Boost = 2f;

	public const string Marker = " +AI";

	private static readonly HashSet<string> AITypes = new HashSet<string> { "AI Assistant", "Coding Assistant", "Image Generator" };

	private float _nextCheck;

	public override void OnActivate()
	{
	}

	public override void OnDeactivate()
	{
		GameSettings gs = GameSettings.Instance;
		if (gs != null && gs.Difficulty != null)
		{
			gs.Difficulty = Toggle(gs.Difficulty, false) ?? gs.Difficulty;
		}
	}

	private void Update()
	{
		if (UnityEngine.Time.unscaledTime < _nextCheck)
		{
			return;
		}
		_nextCheck = UnityEngine.Time.unscaledTime + 5f;
		GameSettings gs = GameSettings.Instance;
		if (gs == null || gs.MyCompany == null || gs.Difficulty == null)
		{
			return;
		}
		gs.Difficulty = Toggle(gs.Difficulty, HasOwnAI(gs.MyCompany)) ?? gs.Difficulty;
	}

	// The difficulty to switch to, or null when it already matches
	public static DifficultyValues.DifficultySetting Toggle(DifficultyValues.DifficultySetting d, bool boosted)
	{
		string name = d.Name ?? "";
		bool isBoosted = name.EndsWith(Marker);
		if (boosted == isBoosted)
		{
			return null;
		}
		float factor = boosted ? Boost : 1f / Boost;
		DifficultyValues.DifficultySetting copy = new DifficultyValues.DifficultySetting(
			boosted ? name + Marker : name.Substring(0, name.Length - Marker.Length), d);
		copy.AlphaSpeedBonus *= factor;
		copy.DesignDocumentSpeedBonus *= factor;
		return copy;
	}

	public static bool HasOwnAI(Company company)
	{
		foreach (SoftwareProduct product in company.Products)
		{
			if (product != null && product.Type != null && AITypes.Contains(product.Type.Name))
			{
				return true;
			}
		}
		return false;
	}
}
